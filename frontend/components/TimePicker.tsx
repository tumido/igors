import { LocalizationProvider, StaticTimePicker } from '@mui/lab'
import DateAdapter from '@mui/lab/AdapterDateFns'
import { DateIOFormats } from '@date-io/core/IUtils'
import csLocale from 'date-fns/locale/cs'
import { Button } from '@mui/material'
import { useState } from 'react'
class CustomDateAdapter extends DateAdapter {
  public format = (date: Date, formatKey: keyof DateIOFormats) => {
    return this.formatByString(date, this.formats[formatKey]) + ' min'
  }
}

const TimePicker = () => {
  const [value, setValue] = useState<Date | null>(new Date(0))

  return (
    <>
      <LocalizationProvider dateAdapter={CustomDateAdapter} locale={csLocale}>
        <StaticTimePicker
          orientation="landscape"
          label="Zapni vyhřívání"
          inputFormat="mm"
          displayStaticWrapperAs="mobile"
          openTo="minutes"
          views={['minutes']}
          value={value}
          onChange={(newValue) => {
            setValue(newValue)
          }}
          renderInput={(params) => <></>}
        />
      </LocalizationProvider>
      <Button variant="contained">Zapni</Button>
    </>
  )
}

export default TimePicker
