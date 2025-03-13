# SA-getcron

## Overview
**SA-getcron** is a Splunk app that provides custom search commands for handling cron expressions. This app helps validate cron expressions, translate them into human-readable formats, and determine previous and next execution schedules.

## Installation
1. Download the **SA-getcron** app.
2. Place the app in your Splunk apps directory: `$SPLUNK_HOME/etc/apps/`.
3. Restart Splunk to load the new commands.

## Custom Search Commands
SA-getcron provides five custom search commands:

### 1. `cronvalidator`
Validates if a value in the `cron` field is a valid cron expression.
- **Returns**: `cron_is_valid` (String: `TRUE` or `FALSE`)
- **Syntax**:
  ```
  | cronvalidator <field>
  ```
- **Default Field**: If the `field` argument is not provided, it defaults to `cron`.

### 2. `getcrondescription`
Converts a cron expression into a human-readable format.
- **Returns**: `cron_description`
- **Syntax**:
  ```
  | getcrondescription <field>
  ```
- **Default Field**: If the `field` argument is not provided, it defaults to `cron`.

### 3. `getcronnextsched`
Returns the next scheduled execution time of the cron expression.
- **Returns**: `cron_next_schedule`
- **Syntax**:
  ```
  | getcronnextsched <field>
  ```
- **Default Field**: If the `field` argument is not provided, it defaults to `cron`.

### 4. `getcronprevsched`
Returns the previous execution time of the cron expression.
- **Returns**: `cron_prev_schedule`
- **Syntax**:
  ```
  | getcronprevsched <field>
  ```
- **Default Field**: If the `field` argument is not provided, it defaults to `cron`.

### 5. `getcrondetails`
Combines all the above commands, returning all fields generated by the first four commands.
- **Returns**: `cron_is_valid`, `cron_description`, `cron_next_schedule`, `cron_prev_schedule`
- **Optional Arguments**:
  - `field`: The field containing the cron expression (defaults to `cron` if not provided).
  - `prefix`: A prefix to add to each output field (defaults to blank, meaning no prefix is added).
- **Syntax**:
  ```
  | getcrondetails <field> <prefix>
  ```

## Examples
### Example 1: Validate a cron expression
```
| makeresults | eval cron="*/5 * * * *" | cronvalidator cron
```

### Example 2: Get a human-readable description of a cron schedule
```
| makeresults | eval cron="0 12 * * MON" | getcrondescription cron
```

### Example 3: Get the next execution schedule of a cron expression
```
| makeresults | eval cron="0 0 1 * *" | getcronnextsched cron
```

### Example 4: Get the previous execution schedule of a cron expression
```
| makeresults | eval cron="0 0 1 * *" | getcronprevsched cron
```

### Example 5: Get all cron-related information with a prefix
```
| makeresults | eval cron="*/10 * * * *" | getcrondetails cron myprefix
```

## Support
For issues or feature requests, please contact the developer or submit an issue in the project repository.
