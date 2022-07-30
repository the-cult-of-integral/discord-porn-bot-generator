import rule34


class LinkGrabber:

    def grab_links(self, tag=str) -> list:
        sync = rule34.Sync()

        print('Finding total media...')
        if (total := sync.totalImages(tag)) == 0:
            return []

        print('Grabbing links...')
        try:
            media = sync.getImages(tag, singlePage=False)
        except Exception:
            return []

        if media is None:
            return []

        print('Filtering images from other links...')
        images = list(filter(
            lambda x: 'webm' not in x.file_url and 'mp4' not in x.file_url, media))

        print(f'{total} images found!')
        return images
