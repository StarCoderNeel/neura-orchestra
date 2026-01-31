"""Tests for Model versioning and tracking feature."""

import pytest
from src.model_feature import ModelFeature, create_feature_instance


class TestModelFeature:
    """Test suite for ModelFeature class."""
    
    @pytest.fixture
    def feature(self):
        """Create a feature instance for testing."""
        return ModelFeature()
    
    @pytest.fixture
    def initialized_feature(self, feature):
        """Create an initialized feature instance."""
        feature.initialize()
        return feature
    
    def test_initialization(self, feature):
        """Test feature can be initialized."""
        assert feature._initialized is False
        result = feature.initialize()
        assert result is True
        assert feature._initialized is True
    
    def test_process_requires_initialization(self, feature):
        """Test that process raises error if not initialized."""
        with pytest.raises(RuntimeError, match="not initialized"):
            feature.process("test data")
    
    def test_process_success(self, initialized_feature):
        """Test successful data processing."""
        result = initialized_feature.process("test input")
        assert result["status"] == "success"
        assert result["processed"] is True
    
    def test_cleanup(self, initialized_feature):
        """Test cleanup resets initialization state."""
        initialized_feature.cleanup()
        assert initialized_feature._initialized is False
    
    def test_factory_function(self):
        """Test factory function creates instance."""
        instance = create_feature_instance()
        assert isinstance(instance, ModelFeature)
    
    def test_factory_with_config(self):
        """Test factory function with configuration."""
        config = {"key": "value"}
        instance = create_feature_instance(config)
        assert instance.config == config


@pytest.mark.parametrize("input_data,expected_status", [
    ("string data", "success"),
    (123, "success"),
    ({"key": "value"}, "success"),
    (["list", "data"], "success"),
])
def test_process_various_inputs(input_data, expected_status):
    """Test processing various input types."""
    feature = create_feature_instance()
    feature.initialize()
    result = feature.process(input_data)
    assert result["status"] == expected_status
