```python
def test_search_available_buses(self):
    """Verify user can search for available buses"""
    self.app.enter_source('Mumbai')
    self.app.enter_destination('Pune')
    self.app.select_journey_date('Sat, 7 Sep')
    self.app.tap_search_button()
    assert self.app.is_bus_list_displayed(), 'Bus list should be displayed after search'
```