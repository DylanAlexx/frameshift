from frameshift.parser.filename import MediaType, classify_filename


def test_classifies_movie() -> None:
    assert classify_filename("Oppenheimer.2023.1080p.BluRay.x264.mkv") is MediaType.MOVIE


def test_classifies_tv_episode_sxe() -> None:
    assert classify_filename("Breaking.Bad.S01E01.1080p.BluRay.x264.mkv") is MediaType.TV_EPISODE


def test_classifies_tv_episode_lowercase() -> None:
    assert classify_filename("breaking.bad.s03e10.1080p.mkv") is MediaType.TV_EPISODE


def test_classifies_tv_episode_x_pattern() -> None:
    assert classify_filename("The.Office.2x14.1080p.WEBRip.mkv") is MediaType.TV_EPISODE


def test_classifies_movie_with_year() -> None:
    assert classify_filename("Parasite (2019) [2160p].mkv") is MediaType.MOVIE
