import { test, expect } from '@playwright/test';

test.describe('Java Tutor Chat Simulation', () => {
  test('single student flow', async ({ page }) => {
    // Navigate to your tutor app
    await page.goto('http://localhost:8501'); // Streamlit default port

    // Simulate student typing a metaphor response
    await page.fill('textarea', 'Cars lined up smallest to largest are like nodes in a linked list');
    await page.click('text=Submit response');

    // Expect tutor feedback to appear
    await expect(page.locator('text=Concept: Linked list')).toBeVisible();
  });

  test('multiple students capacity', async ({ browser }) => {
    const contexts = await Promise.all([
      browser.newContext(),
      browser.newContext(),
      browser.newContext()
    ]);

    const pages = await Promise.all(contexts.map(ctx => ctx.newPage()));

    // Each simulated student interacts
    await Promise.all(pages.map(async (p, i) => {
      await p.goto('http://localhost:8501');
      await p.fill('textarea', `Student ${i} says: ropes and braiding = linked list`);
      await p.click('text=Submit response');
      await expect(p.locator('text=Concept')).toBeVisible();
    }));
  });
});