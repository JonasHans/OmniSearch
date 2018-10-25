module.exports = {
  devServer: {
    headers: {
      'Access-Control-Allow-Origin':
        'http://localhost:9200',
      'Access-Control-Allow-Headers':
        '*',
    }
  }
}