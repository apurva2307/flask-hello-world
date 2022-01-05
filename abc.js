console.log("First");

setTimeout(function () {
  console.log("Second");
}, 0);

new Promise(function (res) {
  res("Third");
}).then(console.log);

console.log("Fourth");
