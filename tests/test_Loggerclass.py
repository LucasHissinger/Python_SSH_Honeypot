from src.Loggerclass import Logger
import logging
import os
import pytest


@pytest.fixture
def logger():
    return Logger("127.0.0.1")


def test_logger_creation(logger):
    assert isinstance(logger.logger, logging.Logger)


def test_logger_info(logger, caplog):
    logger.log_info("This is an info message")
    assert "This is an info message" in caplog.text


def test_logger_warning(logger, caplog):
    logger.log_warning("This is a warning message")
    assert "This is a warning message" in caplog.text


def test_logger_error(logger, caplog):
    logger.log_error("This is an error message")
    assert "This is an error message" in caplog.text


def test_logger_file_creation(logger):
    assert os.path.exists(logger.file)
    assert os.path.isfile(logger.file)
    os.remove(logger.file)
    os.rmdir(os.path.dirname(logger.file))
