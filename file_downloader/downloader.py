import requests
from concurrent.futures import ProcessPoolExecutor


class Downloader:
    def __init__(self, src_url, num_threads):
        try:
            header = requests.head(src_url).headers
            self.url = src_url
            self.file_size = int(header['content-length'])
            self.file_name = src_url.split('/')[-1]
            self.num_threads = num_threads
            self.chunk_size = self.file_size // self.num_threads

            f = open(self.file_name, 'wb')
            f.write(b'\x00' * self.file_size)
            f.close()
        except requests.exceptions.ConnectionError:
            print('Connection error, please check your internet connection.')

    def _worker(self, download_range):
        start, end = download_range

        return True

    def download(self) -> None:
        download_ranges = []

        for i in range(self.num_threads):
            start = i * self.chunk_size
            if i == self.num_threads - 1:
                end = self.file_size
            else:
                end = start + self.chunk_size - 1

            download_ranges.append((start, end))

        print('Downloading...')
        with ProcessPoolExecutor(max_workers=self.num_threads) as executor:
            results = executor.map(self._worker, download_ranges)
