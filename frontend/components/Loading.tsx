import styles from './Loading.module.css'
import { ComponentType } from 'react'

export type LoadingProps = {
  icon: ComponentType
}

const Loading = ({ icon: Icon }: LoadingProps) => {
  return (
    <div className={styles.page}>
      <span className={styles.icon}>{<Icon />}</span>
    </div>
  )
}

export default Loading
