import http from 'k6/http';
import { sleep, check } from 'k6';

const filters = ['rotate', 'greyscale', 'resize', 'flip', 'crop', 'format', 'compress'];

let results = {};
for (const f of filters) {
  results[f] = { total: 0, count: 0 };
}

export let options = {
  vus: 1,
  iterations: filters.length * 10,
};

export default function () {
  const index = Math.floor(__ITER / 10);
  const filter = filters[index];

  const url = `https://rjwr5ytnl3x3xp3ugsjdrp7ywa0rhufh.lambda-url.eu-central-1.on.aws/?filter=${filter}&key=test.jpg`;

  const res = http.get(url);
  const duration = res.timings.duration;

  results[filter].total += duration;
  results[filter].count += 1;

  const avg = results[filter].total / results[filter].count;

  console.log(`${filter.padEnd(10)} | now: ${duration.toFixed(2)} ms | avg: ${avg.toFixed(2)} ms`);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  // === Финальный вывод в самом конце теста
  if (__ITER === (filters.length * 10) - 1) {
    console.log('\n--- FINAL AVERAGE DURATION BY FILTER ---');
    for (const f of filters) {
      const avg = results[f].total / results[f].count;
      console.log(`${f.padEnd(10)} : ${avg.toFixed(2)} ms`);
    }
  }

  sleep(1);
}
