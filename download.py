import sys
import os
import argparse
import requests
import re


class SVGFile:
    url: str
    _path: str

    def __init__(self, url: str, path: str):
        self.url = url
        self._path = path

    def download(self) -> None:
        r = requests.get(self.url, allow_redirects=True)
        if not os.path.exists(self._path):
            os.makedirs(self._path)
        with open(self.get_target_path(), 'wb+') as f:
            f.write(r.content)

    def get_target_path(self):
        url_segments = self.url.rsplit('/', 2)
        file_name = url_segments[-1]
        id = url_segments[-2]
        file_name_with_id = f'{os.path.splitext(file_name)[0]}.{id}.svg'
        return os.path.join(self._path, file_name_with_id)


class SVGCollectionDownloader:
    _base_url: str = None
    _collection_name: str = None
    _svg_files: list[SVGFile] = []
    _path = None

    def __init__(self, url: str, path: str):
        if url[-1] == '/':
            url = url[:-1]
        self._base_url = url.rsplit('/', 1)[0]
        self._collection_name = url.rsplit('/', 1)[-1]
        self._path = path
        print('Downloading collection from', url)

    def download(self) -> None:
        page = 1
        next_page = f'{self._base_url}/{self._collection_name}'
        while page > 0:
            print('Gathering download links from', next_page)
            r = requests.get(next_page, allow_redirects=True)

            # Match anything "/show/[0-9]+/<some name>.svg"
            matches = re.findall(r'"(\/show\/[0-9]+\/[^"]+\.svg)"', r.text)
            for match in matches:
                download_url = f'{self._base_url.rsplit("/", 1)[0]}{match.replace("/show/", "/download/")}'
                if download_url not in self._svg_files:
                    self._svg_files.append(SVGFile(download_url, self._path))

            # Check if we have a next page
            page += 1
            if re.search(f'"/collection/{self._collection_name}/{page}"', r.text) is not None:
                next_page = f'{self._base_url}/{self._collection_name}/{page}'
            else:
                page = 0

        for svg_file in self._svg_files:
            print('Downloading', svg_file.url, 'to', svg_file.get_target_path())
            svg_file.download()


if __name__ == '__main__':
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('url')
    args_parser.add_argument('-p', '--path')

    args = args_parser.parse_args()

    if args.path is None:
        if os.name == 'nt':
            args.path = os.path.join(
                os.path.expandvars('%USERPROFILE%'),
                'Documents',
                'icons'
            )
        else:
            args.path = os.path.join(os.path.expanduser('~'), 'icons')

    svg_collection_downloader = SVGCollectionDownloader(url=args.url, path=args.path)
    svg_collection_downloader.download()
