import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 50,          // 15 users
  duration: '10s',
};

export default function () {
  const url = 'https://rjwr5ytnl3x3xp3ugsjdrp7ywa0rhufh.lambda-url.eu-central-1.on.aws/?key=test.jpg';
  http.get(url);
  sleep(1);
}
