const express = require('express')
const next = require('next')
const { createProxyMiddleware } = require('http-proxy-middleware')

const port = process.env.PORT || 3000
const dev = process.env.NODE_ENV !== 'production'
const app = next({ dev })
const handle = app.getRequestHandler()

const apiPath = {
  target:
    process.env.NODE_ENV === 'stage'
      ? 'http://igor.lan'
      : 'http://127.0.0.1:5000',
  pathRewrite: {
    '^/api': '/api',
  },
}

app
  .prepare()
  .then(() => {
    const server = express()

    server.use('/api', createProxyMiddleware(apiPath))

    server.all('*', (req, res) => {
      return handle(req, res)
    })

    server.listen(port, (err) => {
      if (err) throw err

      console.log(`> Ready on http://localhost:${port}`)
    })
  })
  .catch((err) => {
    console.log(err)
  })
