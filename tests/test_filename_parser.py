from frameshift.models.parsed_media import MediaType
from frameshift.parser.media_parser import parse_filename


def test_classifies_movie() -> None:
    assert parse_filename("Oppenheimer.2023.1080p.BluRay.x264.mkv").media_type is MediaType.MOVIE


def test_classifies_tv_episode_sxe() -> None:
    assert (
        parse_filename("Breaking.Bad.S01E01.1080p.BluRay.x264.mkv").media_type
        is MediaType.TV_EPISODE
    )


def test_classifies_tv_episode_lowercase() -> None:
    assert parse_filename("breaking.bad.s03e10.1080p.mkv").media_type is MediaType.TV_EPISODE


def test_classifies_tv_episode_x_pattern() -> None:
    assert parse_filename("The.Office.2x14.1080p.WEBRip.mkv").media_type is MediaType.TV_EPISODE


def test_classifies_movie_with_year() -> None:
    assert parse_filename("Parasite (2019) [2160p].mkv").media_type is MediaType.MOVIE


def test_parses_movie_title_and_year() -> None:
    parsed = parse_filename("Oppenheimer.2023.1080p.BluRay.x264.mkv")

    assert parsed.media_type is MediaType.MOVIE
    assert parsed.title == "Oppenheimer"
    assert parsed.year == 2023


def test_parses_movie_with_brackets() -> None:
    parsed = parse_filename("Parasite (2019) [2160p].mkv")

    assert parsed.title == "Parasite"
    assert parsed.year == 2019


def test_parses_tv_show_title_season_episode() -> None:
    parsed = parse_filename("Breaking.Bad.S01E01.1080p.BluRay.x264.mkv")

    assert parsed.media_type is MediaType.TV_EPISODE
    assert parsed.title == "Breaking Bad"
    assert parsed.season == 1
    assert parsed.episode == 1


def test_parses_tv_show_x_format() -> None:
    parsed = parse_filename("The.Office.2x14.1080p.WEBRip.mkv")

    assert parsed.media_type is MediaType.TV_EPISODE
    assert parsed.title == "The Office"
    assert parsed.season == 2
    assert parsed.episode == 14


def test_parses_1080p_resolution() -> None:
    parsed = parse_filename("Oppenheimer.2023.1080p.BluRay.x264.mkv")

    assert parsed.resolution == "1080p"


def test_parses_2160p_resolution() -> None:
    parsed = parse_filename("The.Batman.2022.2160p.WEB.x265.mkv")

    assert parsed.resolution == "2160p"
