import { MouseEventHandler } from 'react'
import styles from './HeaterCard.module.css'

export type HeaterCardProps = {
  value: Boolean | null
  onClick: MouseEventHandler
}

const WeatherCard = ({ value, onClick }: HeaterCardProps) => {
  return (
    <div className={`${styles.widget} ${value && styles.on}`} onClick={onClick}>
      <span className={styles.value}>
        {value ? 'On' : value === null ? '?' : 'Off'}
      </span>
    </div>
  )
}

export default WeatherCard
