import { mkdir, readFileSync, writeFileSync } from 'fs'
import type { NextApiRequest, NextApiResponse } from 'next'

export type IgorsData = {
  heater: Boolean | null
  above: Number
  below: Number
  humidity: Number
}
type Success = {
  message: string
}

const readNumberFromFile = (path: string): Number => {
  try {
    return Number(readFileSync(path).toString())
  } catch {
    return 0
  }
}

const readPowerFromFile = (path: string): Boolean | null => {
  try {
    const text = readFileSync(path).toString()

    switch (text) {
      case 'on':
        return true
      case 'off':
        return false
      default:
        return null
    }
  } catch {
    return null
  }
}

const getData = (): IgorsData => ({
  above: readNumberFromFile('/tmp/dht/temp'),
  below: readNumberFromFile('/tmp/ds/temp'),
  humidity: readNumberFromFile('/tmp/dht/humidity'),
  heater: readPowerFromFile('/tmp/relay/power'),
})

const handler = (
  req: NextApiRequest,
  res: NextApiResponse<IgorsData | Success>
) => {
  switch (req.method) {
    case 'GET':
      res.status(200).json(getData())
      break
    case 'POST':
      console.log(req.body)
      mkdir('/tmp/relay', () => {})
      writeFileSync('/tmp/relay/power', req.body.heater ? 'on' : 'off')
      res.status(200).json({ message: 'Success' })
      break
    default:
      res.status(405)
  }
}

export default handler
