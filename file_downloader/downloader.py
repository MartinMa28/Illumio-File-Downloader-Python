import requests
from multiprocessing import Process
from atomic_counter import AtomicCounter


class Downloader:
    def __init__(self, src_url, num_threads):
        try:
            header = requests.head(src_url).headers
            self.url = src_url
            self.file_size = int(header.get('content-length'))
            self.file_name = src_url.split('/')[-1]
            self.num_threads = num_threads
            self.chunk_size = self.file_size // self.num_threads

            with open(self.file_name, 'wb') as f:
                f.write(b'\x00' * self.file_size)

        except requests.exceptions.ConnectionError:
            print('Connection error, please check your internet connection.')

    def _worker(self, download_range: tuple, counter: AtomicCounter):
        start, end = download_range
        header = {'Range': 'bytes=' + str(start) + '-' + str(end)}
        
        r = requests.get(self.url, headers=header, stream=True, timeout=30)
        binary_content = r.content
        counter.increment_by_value(end - start + 1)
        print(counter.get_value() / self.file_size)

        with open(self.file_name, 'wb') as f:
            f.seek(start)
            f.write(binary_content)

    def download(self) -> None:
        download_ranges = []

        for i in range(self.num_threads):
            start = i * self.chunk_size
            if i == self.num_threads - 1:
                end = self.file_size
            else:
                end = start + self.chunk_size - 1

            download_ranges.append((start, end))

        atomic_counter = AtomicCounter()
        process_pool = [Process(target=self._worker,
                        args=(download_ranges[i], atomic_counter))
                        for i in range(self.num_threads)]

        for p in process_pool:
            p.start()

        for p in process_pool:
            p.join()


if __name__ == "__main__":
    downloader = Downloader('https://download-cf.jetbrains.com/idea/ideaIC-2019.3.3.tar.gz', 4)
    downloader.download()
