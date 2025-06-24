const express = require('express');
const router = express.Router();

router.post('/', (req, res) => {
  const { birth, lifeExpectancy } = req.body;

  const birthDate = new Date(birth);
  const now = new Date();

  const livedMs = now - birthDate;
  const totalMs = lifeExpectancy * 365.25 * 24 * 60 * 60 * 1000;

  const percentage = (livedMs / totalMs) * 100;

  res.json({
    percentage: parseFloat(percentage.toFixed(2))
  });
});

module.exports = router;
