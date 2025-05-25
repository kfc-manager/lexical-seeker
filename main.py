from crawler import crawl


BEGIN_TOKEN = "<|bos|>"
END_TOKEN = "<|eos|>"
PADDING_TOKEN = "<|pad|>"
UNKNOWN_TOKEN = "<|unk|>"


def main():
    crawl(
        start="United_States",
        tokens=[BEGIN_TOKEN, END_TOKEN, PADDING_TOKEN, UNKNOWN_TOKEN],
    )


if __name__ == "__main__":
    main()
