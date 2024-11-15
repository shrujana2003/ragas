import os
import pytest
import asyncio
from unittest.mock import patch, mock_open
from docs.alfred import get_files, load_docs, File
from langchain.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai.chat_models import ChatOpenAI

@pytest.fixture
def mock_get_files():
    with patch('docs.alfred.get_files') as mock:
        mock.return_value = ['test_directory/file1.md', 'test_directory/file2.md']
        yield mock

@pytest.fixture
def mock_load_docs():
    with patch('docs.alfred.load_docs') as mock:
        mock.return_value = [
            File(name='test_directory/file1.md', content='Content of file1'),
            File(name='test_directory/file2.md', content='Content of file2')
        ]
        yield mock

@pytest.fixture
def mock_open_file():
    m = mock_open(read_data='Content of file1')
    with patch('builtins.open', m):
        yield m

@pytest.fixture
def mock_chat_openai():
    with patch('docs.alfred.ChatOpenAI') as mock:
        instance = mock.return_value
        instance.ainvoke.return_value = File(name='test_directory/file1.md', content='Fixed content of file1')
        yield instance

@pytest.fixture
def mock_tqdm():
    with patch('tqdm.asyncio.tqdm') as mock:
        yield mock

# happy path - get_files - Test that get_files returns a list of files with the specified extension in the given directory.
def test_get_files_with_md_extension(mock_get_files):
    path = 'test_directory'
    ext = '.md'
    result = get_files(path, ext)
    assert result == ['test_directory/file1.md', 'test_directory/file2.md']


# happy path - load_docs - Test that load_docs loads markdown files and returns a list of File namedtuples with correct content.
def test_load_docs_with_md_files(mock_load_docs, mock_open_file):
    path = 'test_directory'
    result = load_docs(path)
    expected = [
        File(name='test_directory/file1.md', content='Content of file1'),
        File(name='test_directory/file2.md', content='Content of file2')
    ]
    assert result == expected


# happy path - get_files - Test that get_files returns an empty list when no files with the specified extension are present.
def test_get_files_no_matching_extension():
    with patch('docs.alfred.get_files', return_value=[]) as mock_get_files:
        path = 'test_directory'
        ext = '.txt'
        result = get_files(path, ext)
        assert result == []


# happy path - load_docs - Test that load_docs returns an empty list when there are no markdown files in the directory.
def test_load_docs_no_md_files():
    with patch('docs.alfred.load_docs', return_value=[]) as mock_load_docs:
        path = 'empty_directory'
        result = load_docs(path)
        assert result == []


# happy path - get_files - Test that get_files correctly handles directories with a large number of files.
def test_get_files_large_directory():
    with patch('docs.alfred.get_files', return_value=[
        'large_directory/file1.md',
        'large_directory/file2.md',
        'large_directory/file3.md'
    ]) as mock_get_files:
        path = 'large_directory'
        ext = '.md'
        result = get_files(path, ext)
        assert result == [
            'large_directory/file1.md',
            'large_directory/file2.md',
            'large_directory/file3.md'
        ]


# edge case - get_files - Test that get_files returns an empty list when the directory does not exist.
def test_get_files_non_existent_directory():
    with patch('os.listdir', side_effect=FileNotFoundError):
        path = 'non_existent_directory'
        ext = '.md'
        result = get_files(path, ext)
        assert result == []


# edge case - load_docs - Test that load_docs raises an error when the directory does not exist.
def test_load_docs_non_existent_directory():
    with patch('os.listdir', side_effect=FileNotFoundError):
        path = 'non_existent_directory'
        try:
            load_docs(path)
            assert False, "Expected FileNotFoundError"
        except FileNotFoundError:
            assert True


# edge case - get_files - Test that get_files handles directories with files having no extension.
def test_get_files_no_extension():
    with patch('docs.alfred.get_files', return_value=[]) as mock_get_files:
        path = 'no_extension_directory'
        ext = '.md'
        result = get_files(path, ext)
        assert result == []


# edge case - load_docs - Test that load_docs handles files with special characters in their names.
def test_load_docs_special_characters(mock_open_file):
    with patch('docs.alfred.get_files', return_value=[
        'special_char_directory/file@1.md',
        'special_char_directory/file#2.md'
    ]) as mock_get_files:
        path = 'special_char_directory'
        result = load_docs(path)
        expected = [
            File(name='special_char_directory/file@1.md', content='Content of file@1'),
            File(name='special_char_directory/file#2.md', content='Content of file#2')
        ]
        assert result == expected


# edge case - get_files - Test that get_files handles directories with mixed file types and returns only the specified extension.
def test_get_files_mixed_types():
    with patch('docs.alfred.get_files', return_value=[
        'mixed_types_directory/file1.md',
        'mixed_types_directory/file2.md'
    ]) as mock_get_files:
        path = 'mixed_types_directory'
        ext = '.md'
        result = get_files(path, ext)
        assert result == [
            'mixed_types_directory/file1.md',
            'mixed_types_directory/file2.md'
        ]


