const express = require('express');
const app = express();
const lifeRouter = require('./routes/life');

app.use(express.json());
app.use('/life', lifeRouter);  

app.listen(3000, () => {
  console.log('서버 실행 중: http://localhost:3000');
});