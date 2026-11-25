---
name: polaris-pattern-date-picking
description: Let merchants pick dates confidently—calendar picker with keyboard input for schedule events and memorable dates
---

# Date Picking

Lets merchants select a date or a date range.

## How it helps merchants

- **Text input**: Merchants can use the keyboard to enter a date directly
- **Calendar**: Single month calendar shows date relationships to other days, enabling confident selection

## Use when merchants need to:

- **Schedule an event on a specific day**: Setting visibility date for a page, estimated arrival date for shipment (found in Product/transfers)
- **Input memorable dates to forms**: Entering a birthdate or other specific dates

## Components Used

- Card
- DatePicker
- Popover
- TextField

## Pattern structure

```jsx
const [visible, setVisible] = useState(false);
const [selectedDate, setSelectedDate] = useState(new Date());
const [{ month, year }, setDate] = useState({
  month: selectedDate.getMonth(),
  year: selectedDate.getFullYear(),
});
const formattedValue = selectedDate.toISOString().slice(0, 10);
const datePickerRef = useRef(null);

return (
  <Box minWidth="276px" padding={{ xs: 200 }}>
    <Popover
      active={visible}
      autofocusTarget="none"
      preferredAlignment="left"
      fullWidth
      preferInputActivator={false}
      preferredPosition="below"
      preventCloseOnChildOverlayClick
      onClose={() => setVisible(false)}
      activator={
        <TextField
          role="combobox"
          label="Start date"
          prefix={<Icon source={CalendarIcon} />}
          value={formattedValue}
          onFocus={() => setVisible(true)}
          onChange={handleInputValueChange}
          autoComplete="off"
        />
      }
    >
      <Card ref={datePickerRef}>
        <DatePicker
          month={month}
          year={year}
          selected={selectedDate}
          onMonthChange={handleMonthChange}
          onChange={handleDateSelection}
        />
      </Card>
    </Popover>
  </Box>
);
```

## Guidelines

- Labels should simply depict the task at hand (e.g., "Start date", "End date", "Start time")
- This pattern can be duplicated to allow users to add an end date or time
- Keep date formatting consistent across your app

## Date range pattern

Duplicate the single date pattern to create date range selectors. One for start date, one for end date.

## Notes on date handling

- Timezones can be finicky—keep them consistent
- Use ISO 8601 format (YYYY-MM-DD) internally for consistency
- Display dates in merchant's preferred format
