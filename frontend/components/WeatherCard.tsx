import styles from './WeatherCard.module.css'
import { ComponentType } from 'react'

export type WeatherCardProps = {
  value: Number
  type: 'temperature' | 'humidity'
  icon?: ComponentType
}

const WeatherCard = ({ value, icon: Icon, type }: WeatherCardProps) => {
  return (
    <div className={styles.widget}>
      <span className={styles.value}>{value}</span>
      <span className={styles.unit}>{type == 'temperature' ? '˚C' : '%'}</span>
      <span className={styles.icon}>{Icon && <Icon />}</span>
    </div>
  )
}

export default WeatherCard
