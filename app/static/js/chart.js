function drawPieChart(percentages) {
const labels = ['5', '4', '3', '2', '1'];
const scaleFactor = 2;
  // 获取 canvas 元素
  const canvas = document.getElementById('myCanvas');
  const ctx = canvas.getContext('2d');

  // 计算饼图的角度
  const total = percentages.reduce((a, b) => a + b, 0);
  const angles = percentages.map(p => p / 100 * 2 * Math.PI);

  // 绘制饼图
  let startAngle = 0;
  for (let i = 0; i < percentages.length; i++) {
    const endAngle = startAngle + angles[i];
    ctx.beginPath();
    ctx.moveTo(200, 200);
    ctx.arc(200, 200, 80 * scaleFactor, startAngle, endAngle);
    ctx.closePath();
    ctx.fillStyle = `hsl(${i * 50}, 70%, 50%)`;
    ctx.fill();
    startAngle = endAngle;

  }

  // 绑定单击事件，触发另一个JavaScript文件的执行
  canvas.addEventListener('click', function(event) {
    // 获取鼠标单击的坐标
    const x = event.offsetX;
    const y = event.offsetY;

    // 判断鼠标单击的位置是否在饼图中
    const distance = Math.sqrt((x - 200) ** 2 + (y - 200) ** 2);
    if (distance <= 80 * scaleFactor) {
      // 计算鼠标单击的角度
      var angle = Math.atan2(y - 200, x - 200);
      if (angle < 0) {
        angle += 2 * Math.PI;
      }

      // 计算鼠标单击的区域
      let cumulativeAngle = 0;
      for (let i = 0; i < percentages.length; i++) {
        cumulativeAngle += angles[i];
        if (angle < cumulativeAngle) {
          // 执行另一个JavaScript文件的代码
          showImage(labels[i])
          console.log(`点击了第${i + 1}个区域，注解为：${labels[i]}`);
          break;
        }
      }
    }
  });
}
