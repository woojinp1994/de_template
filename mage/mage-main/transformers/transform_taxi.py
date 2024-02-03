import inflection

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):

    data = data[(data['passenger_count'] != 0) ]
    data = data[(data['trip_distance'] != 0) ]

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    old_columns = data.columns
    new_columns = [inflection.underscore(x) for x in data.columns]
    data.columns = new_columns

    # For homework: checking values in dataframe
    print(f'Values in vendor_id: {data.vendor_id.unique().tolist()}')
    print(f'Columns that require re-naming: {list(set(old_columns) - set(new_columns))}')

    return data
    

@test
def test_output(output, *args) -> None:
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers.'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distances'
    assert 'vendor_id' in output.columns, 'vendor_id does not exist as a column'