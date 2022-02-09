import { LocalizationProvider, StaticTimePicker } from '@mui/lab'
import DateAdapter from '@mui/lab/AdapterDateFns'
import { DateIOFormats } from '@date-io/core/IUtils'
import csLocale from 'date-fns/locale/cs'
class CustomDateAdapter extends DateAdapter {
  public format = (date: Date, formatKey: keyof DateIOFormats) => {
    return this.formatByString(date, this.formats[formatKey]) + ' min'
  }
}

type TimePickerProps = {
  value: Date | null
  onChange: (value: Date | null) => void
}

const TimePicker = ({ value, onChange }: TimePickerProps) => {
  return (
    <LocalizationProvider dateAdapter={CustomDateAdapter} locale={csLocale}>
      <StaticTimePicker
        label="Zapni vyhřívání"
        inputFormat="mm"
        openTo="minutes"
        views={['minutes']}
        value={value}
        onChange={onChange}
        renderInput={(params) => <></>}
      />
    </LocalizationProvider>
  )
}

export default TimePicker
