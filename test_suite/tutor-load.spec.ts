import { test, expect } from '@playwright/test';

const STUDENT_COUNT = 50; // scale up/down
const BASE_URL = 'http://localhost:8501'; // Streamlit default

test.describe('Java Tutor Load Test', () => {
  test('simulate multiple students concurrently', async ({ browser }) => {
    const contexts = await Promise.all(
      Array.from({ length: STUDENT_COUNT }, () => browser.newContext())
    );
    const pages = await Promise.all(contexts.map(ctx => ctx.newPage()));

    const start = Date.now();

    await Promise.all(pages.map(async (page, i) => {
      await page.goto(BASE_URL);

      // Each student submits a metaphor response
      const responseText = `Student ${i} says: cars in a lot = linked list`;
      await page.fill('textarea', responseText);
      await page.click('text=Submit response');

      // Expect tutor feedback
      await expect(page.locator('text=Concept')).toBeVisible({ timeout: 10000 });
    }));

    const duration = Date.now() - start;
    console.log(`Simulated ${STUDENT_COUNT} students in ${duration}ms`);
  });
});