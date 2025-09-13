import pytest
from unittest import mock
from domain.logic.data.person import Person
from src.application.eligibility.eligibility_service import EligibilityService

@pytest.fixture
def mock_dependencies():
    with mock.patch("src.application.eligibility.eligibility_service.EligibilityRepository") as MockRepo, \
         mock.patch("src.application.eligibility.eligibility_service.Notifier") as MockNotifier, \
         mock.patch("src.application.eligibility.eligibility_service.BlobUploader") as MockUploader, \
         mock.patch("src.application.eligibility.eligibility_service.DummyEligibilityDataGenerator") as MockGenerator, \
         mock.patch("src.application.eligibility.eligibility_service.EligibilityTransformer") as MockTransformer:
        yield {
            "MockRepo": MockRepo,
            "MockNotifier": MockNotifier,
            "MockUploader": MockUploader,
            "MockGenerator": MockGenerator,
            "MockTransformer": MockTransformer,
        }

def make_config(add_dummy=False):
    return {
        "client_ids": ["123", "456"],
        "eff_dt": "2023-01-01",
        "end_dt": "2023-12-31",
        "layout_cols": ["col1", "col2"],
        "add_dummy": add_dummy,
    }

def test_run_with_data_no_dummy(mock_dependencies):
    # Arrange
    config = make_config(add_dummy=False)
    mock_repo = mock_dependencies["MockRepo"].return_value
    mock_notifier = mock_dependencies["MockNotifier"].return_value
    mock_uploader = mock_dependencies["MockUploader"].return_value
    mock_generator = mock_dependencies["MockGenerator"].return_value
    mock_transformer = mock_dependencies["MockTransformer"].return_value

    mock_df = mock.Mock()
    mock_df.count.return_value = 1
    mock_repo.read_eligibility.return_value = mock_df

    mock_pdf = mock.Mock()
    mock_pdf.to_csv.return_value = "csvdata"
    mock_transformer.transform.return_value = mock_pdf

    service = EligibilityService(spark=mock.Mock(), config=config)

    # Act
    service.run()

    # Assert
    mock_repo.read_eligibility.assert_called_once_with("client_filter", "2023-01-01", "2023-12-31")
    mock_notifier.send_no_data_alert.assert_not_called()
    mock_generator.generate.assert_not_called()
    mock_df.unionByName.assert_not_called()
    mock_transformer.transform.assert_called_once_with(mock_df)
    mock_pdf.to_csv.assert_called_once_with(index=False)
    mock_uploader.upload_csv.assert_called_once()
    args, kwargs = mock_uploader.upload_csv.call_args
    assert args[0] == "Eligibility_123_456.csv"
    assert args[1] == b"csvdata"

def test_run_with_data_and_dummy(mock_dependencies):
    # Arrange
    config = make_config(add_dummy=True)
    mock_repo = mock_dependencies["MockRepo"].return_value
    mock_notifier = mock_dependencies["MockNotifier"].return_value
    mock_uploader = mock_dependencies["MockUploader"].return_value
    mock_generator = mock_dependencies["MockGenerator"].return_value
    mock_transformer = mock_dependencies["MockTransformer"].return_value

    mock_df = mock.Mock()
    mock_df.count.return_value = 1
    mock_repo.read_eligibility.return_value = mock_df

    mock_dummy_df = mock.Mock()
    mock_generator.generate.return_value = mock_dummy_df

    mock_union_df = mock.Mock()
    mock_df.unionByName.return_value = mock_union_df

    mock_pdf = mock.Mock()
    mock_pdf.to_csv.return_value = "csvdata"
    mock_transformer.transform.return_value = mock_pdf

    service = EligibilityService(spark=mock.Mock(), config=config)

    # Act
    service.run()

    # Assert
    mock_repo.read_eligibility.assert_called_once_with("client_filter", "2023-01-01", "2023-12-31")
    mock_generator.generate.assert_called_once_with("client_filter")
    mock_df.unionByName.assert_called_once_with(mock_dummy_df)
    mock_transformer.transform.assert_called_once_with(mock_union_df)
    mock_pdf.to_csv.assert_called_once_with(index=False)
    mock_uploader.upload_csv.assert_called_once()
    args, kwargs = mock_uploader.upload_csv.call_args
    assert args[0] == "Eligibility_123_456.csv"
    assert args[1] == b"csvdata"

def test_run_with_no_data_raises_and_notifies(mock_dependencies):
    # Arrange
    config = make_config(add_dummy=False)
    mock_repo = mock_dependencies["MockRepo"].return_value
    mock_notifier = mock_dependencies["MockNotifier"].return_value
    mock_uploader = mock_dependencies["MockUploader"].return_value

    mock_df = mock.Mock()
    mock_df.count.return_value = 0
    mock_repo.read_eligibility.return_value = mock_df

    service = EligibilityService(spark=mock.Mock(), config=config)

    # Act / Assert
    with pytest.raises(Exception, match="No eligibility data found."):
        service.run()

    mock_repo.read_eligibility.assert_called_once_with("client_filter", "2023-01-01", "2023-12-31")
    mock_notifier.send_no_data_alert.assert_called_once_with(["123", "456"])
    mock_uploader.upload_csv.assert_not_called()

def test_get_age_with_age_eighteen_should_return_true():

    # Arrange
    expected_age = 18
    sut = Person("John Doe", expected_age)
    
    # Act
    result = sut.get_age()
    
    # Assert
    assert result is expected_age, f"Expected age {expected_age}, but got {result}"