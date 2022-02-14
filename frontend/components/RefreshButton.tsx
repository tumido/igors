import styles from './RefreshButton.module.css'
import RefreshOutlined from '@mui/icons-material/RefreshOutlined'
import { MouseEventHandler } from 'react'
import { mutate } from 'swr'

const RefreshButton = () => {
  const handleClick: MouseEventHandler = (_event) => {
    mutate('/api/igors')
  }
  return (
    <div className={styles.button} onClick={handleClick}>
      <RefreshOutlined />
    </div>
  )
}

export default RefreshButton
