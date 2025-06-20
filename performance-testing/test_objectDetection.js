import http from 'k6/http';

export let options = {
  vus: 1,
  iterations: 10,
};

export default function () {
  const url = 'https://se3rs6chxz4nfkwoaui4epkv7q0setfr.lambda-url.eu-central-1.on.aws/?key=test.jpg';
  http.get(url);
}
