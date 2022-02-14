import { KeyboardEvent, MouseEvent, MouseEventHandler, useState } from 'react'
import styles from './HeaterCard.module.css'
import TimePicker from '../components/TimePicker'
import { useSWRConfig } from 'swr'
import { Drawer, Modal } from '@mui/material'

export type HeaterCardProps = {
  value: Boolean | null
}
type PostPayload = {
  heater: Boolean
  timeout?: Number
}

const WeatherCard = ({ value = false }: HeaterCardProps) => {
  const [ensureTime, setEnsureTime] = useState<Date | null>(new Date(0))
  const [showTimePicker, setShowTimePicker] = useState(value)
  const { mutate } = useSWRConfig()

  const handleHeaterChange = (value: PostPayload) => {
    fetch('/api/igors', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(value),
    }).then(() => mutate('/api/igors'))
  }

  const handleClick: MouseEventHandler = (_event) => {
    if (showTimePicker) {
      setShowTimePicker(false)
    } else if (value) {
      handleHeaterChange({ heater: false })
    } else {
      setEnsureTime(new Date(0))
      setShowTimePicker(true)
    }
  }

  const handleSetEnsureTime = (date: Date | null) => {
    setEnsureTime(date)
    if (date) {
      handleHeaterChange({ heater: true, timeout: date.getMinutes() })
    }
  }
  const toggleDrawer =
    (open: boolean) => (event: KeyboardEvent | MouseEvent) => {
      if (
        event.type === 'keydown' &&
        ((event as KeyboardEvent).key === 'Tab' ||
          (event as KeyboardEvent).key === 'Shift')
      ) {
        return
      }
      setShowTimePicker(open)
    }

  return (
    <div
      className={`${styles.widget} ${value && styles.on}`}
      onClick={handleClick}
    >
      <span className={styles.value}>
        {value ? 'On' : value === null ? '?' : 'Off'}
      </span>
      <Drawer
        anchor="right"
        open={!!showTimePicker}
        onClose={toggleDrawer(false)}
      >
        <TimePicker value={ensureTime} onChange={handleSetEnsureTime} />
      </Drawer>
    </div>
  )
}

export default WeatherCard
