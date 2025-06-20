import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 50,          // 15 виртуальных пользователей
  duration: '10s',  // на протяжении 10 секунд
};

export default function () {
  const url = 'https://se3rs6chxz4nfkwoaui4epkv7q0setfr.lambda-url.eu-central-1.on.aws/?key=test.jpg';  // ЗАМЕНИ на свой Lambda URL
  http.get(url);
  sleep(1);
}