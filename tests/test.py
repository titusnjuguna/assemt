import pytest
from reconciler.views import reconcile
import pandas as pd
import os
from engine import settings
source_path = os.path.join(settings.BASE_DIR, 'Source (2).csv')
target_path = os.path.join(settings.BASE_DIR,  'Target - Target.csv(1).csv')

@pytest.fixture
def sample_data():
    source_data = {'ID': [1, 2, 3], 'Name': ['Alice', 'Bob', 'Charlie']}
    target_data = {'ID': [1, 2, 4], 'Name': ['Alice', 'Bob', 'David']}
    source_df = pd.DataFrame(source_data)
    target_df = pd.DataFrame(target_data)
    return source_df, target_df

def test_reconcile(sample_data):
    source_df, target_df = sample_data
    missing_in_target, missing_in_source, discrepancies = reconcile( source_path,target_path)
    assert missing_in_target['unique'].tolist() == [3]
    assert missing_in_source['unique'].tolist() == [4]
    assert discrepancies['unique'].tolist() == [2]
