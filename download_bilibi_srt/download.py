import re
import requests


def obtain_cc_subtitle(avid="77948393"):
    """obtain cc subtitles
    @avid: id of the video
    """
    url = f"https://www.bilibili.com/video/av{avid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    subtitle_urls = re.findall(r"subtitle_url\":\"(.*?json)", r.text)
    if not subtitle_urls:
        print("There is no cc subtitle in this video!")
        return

    for url in subtitle_urls:
        url = url.replace("\\u002F", "/")
        r = requests.get(url, headers=headers)
        convert_to_srt(url.split("/")[-1].split(".")[0], r.json()["body"])


def convert_to_srt(srt_id, subtitles):
    """convert cc subtitles to srt subtitles
    @subtitles: a json foramt cc subtitles
    """
    srt = []
    for index, subtitle in enumerate(subtitles):
        srt_tmp = f"""{index}\n{subtitle["from"]} --> {subtitle["to"]}\n{subtitle["content"]}\n"""
        srt.append(srt_tmp)

    with open(f"{srt_id}.srt", "w", encoding="utf-8") as f:
        f.write("\n".join(srt))


if __name__ == "__main__":
    obtain_cc_subtitle("68592755")