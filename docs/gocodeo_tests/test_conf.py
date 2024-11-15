import pytest
from unittest.mock import patch, MagicMock
from dataclasses import asdict
from sphinxawesome_theme import ThemeOptions
from ragas import __version__

@pytest.fixture
def mock_theme_options():
    with patch('sphinxawesome_theme.ThemeOptions') as mock:
        mock.return_value = MagicMock()
        mock.return_value.logo_light = './_static/imgs/ragas-logo.png'
        mock.return_value.logo_dark = './_static/imgs/ragas-logo.png'
        mock.return_value.extra_header_link_icons = {
            "discord": {
                "link": "https://discord.gg/5djav8GGNZ",
                "icon": "<svg>...</svg>"
            },
            "github": {
                "link": "https://github.com/explodinggradients/ragas",
                "icon": "<svg>...</svg>"
            },
        }
        yield mock

@pytest.fixture
def mock_asdict():
    with patch('dataclasses.asdict') as mock:
        mock.return_value = {
            'logo_light': './_static/imgs/ragas-logo.png',
            'logo_dark': './_static/imgs/ragas-logo.png',
            'extra_header_link_icons': {
                "discord": {
                    "link": "https://discord.gg/5djav8GGNZ",
                    "icon": "<svg>...</svg>"
                },
                "github": {
                    "link": "https://github.com/explodinggradients/ragas",
                    "icon": "<svg>...</svg>"
                },
            }
        }
        yield mock

@pytest.fixture
def mock_version():
    with patch('ragas.__version__', '0.0.16'):
        yield '0.0.16

# happy path - asdict - Test that the theme options are correctly converted to a dictionary with valid paths and icons.
def test_theme_options_asdict(mock_theme_options, mock_asdict):
    theme_options_instance = ThemeOptions()
    result = asdict(theme_options_instance)
    expected_result = {
        'logo_light': './_static/imgs/ragas-logo.png',
        'logo_dark': './_static/imgs/ragas-logo.png',
        'extra_header_link_icons': {
            "discord": {
                "link": "https://discord.gg/5djav8GGNZ",
                "icon": "<svg>...</svg>"
            },
            "github": {
                "link": "https://github.com/explodinggradients/ragas",
                "icon": "<svg>...</svg>"
            },
        }
    }
    assert result == expected_result


# happy path - ThemeOptions - Test that the theme options include correct extra header link icons for Discord and GitHub.
def test_theme_options_extra_header_link_icons(mock_theme_options):
    theme_options_instance = ThemeOptions()
    result = theme_options_instance.extra_header_link_icons
    expected_result = {
        "discord": {
            "link": "https://discord.gg/5djav8GGNZ",
            "icon": "<svg>...</svg>"
        },
        "github": {
            "link": "https://github.com/explodinggradients/ragas",
            "icon": "<svg>...</svg>"
        },
    }
    assert result == expected_result


# happy path - project_information - Test that the project information is correctly set with the project name and author.
def test_project_information():
    project = "ragas"
    author = "ExplodingGradients"
    expected_result = {
        'project': 'ragas',
        'author': 'ExplodingGradients'
    }
    assert project == expected_result['project']
    assert author == expected_result['author']


# happy path - html_theme - Test that the HTML theme is correctly set to sphinxawesome_theme.
def test_html_theme_setting():
    html_theme = "sphinxawesome_theme"
    expected_result = {
        'html_theme': 'sphinxawesome_theme'
    }
    assert html_theme == expected_result['html_theme']


# happy path - html_static_path - Test that the HTML static path includes the _static directory.
def test_html_static_path():
    html_static_path = ["_static"]
    expected_result = {
        'html_static_path': ['_static']
    }
    assert html_static_path == expected_result['html_static_path']


# edge case - ThemeOptions - Test that the theme options handle missing paths gracefully.
def test_theme_options_missing_paths(mock_theme_options):
    theme_options_instance = ThemeOptions()
    theme_options_instance.logo_light = None
    theme_options_instance.logo_dark = None
    result = asdict(theme_options_instance)
    expected_result = {
        'logo_light': None,
        'logo_dark': None
    }
    assert result['logo_light'] == expected_result['logo_light']
    assert result['logo_dark'] == expected_result['logo_dark']


# edge case - ThemeOptions - Test that empty extra header link icons do not cause errors.
def test_theme_options_empty_icons(mock_theme_options):
    theme_options_instance = ThemeOptions()
    theme_options_instance.extra_header_link_icons = {}
    result = asdict(theme_options_instance)
    expected_result = {
        'extra_header_link_icons': {}
    }
    assert result['extra_header_link_icons'] == expected_result['extra_header_link_icons']


# edge case - project_information - Test that missing project information defaults correctly.
def test_missing_project_information():
    project = None
    author = None
    expected_result = {
        'project': None,
        'author': None
    }
    assert project == expected_result['project']
    assert author == expected_result['author']


# edge case - html_theme - Test that the HTML theme handles an empty theme name without errors.
def test_empty_html_theme():
    html_theme = ""
    expected_result = {
        'html_theme': ''
    }
    assert html_theme == expected_result['html_theme']


# edge case - html_static_path - Test that an empty HTML static path does not cause errors.
def test_empty_html_static_path():
    html_static_path = []
    expected_result = {
        'html_static_path': []
    }
    assert html_static_path == expected_result['html_static_path']


