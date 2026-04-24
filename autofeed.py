"""
Automated UI Test for Student Performance Prediction System
Uses Playwright to simulate real browser interactions on the Streamlit app.

Install:
    pip install playwright
    playwright install chromium

Run:
    python autofeed.py
"""

import asyncio
from playwright.async_api import async_playwright

APP_URL = "http://localhost:8501"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

test_students = [
    # --- POOR (5 cases) ---
    {
        "name": "Ravi Kumar",       "age": 18, "absences": 15,
        "study": "<1 hr",           "consistency": "Rarely",
        "assignment": "Low",        "participation": "Low",
        "prev_grade": "<50",        "sleep": "<5 hrs",
        "expected": "Poor"
    },
    {
        "name": "Priya Nair",       "age": 19, "absences": 18,
        "study": "<1 hr",           "consistency": "Rarely",
        "assignment": "Low",        "participation": "Low",
        "prev_grade": "<50",        "sleep": "<5 hrs",
        "expected": "Poor"
    },
    {
        "name": "Suresh Babu",      "age": 20, "absences": 20,
        "study": "<1 hr",           "consistency": "Rarely",
        "assignment": "Low",        "participation": "Low",
        "prev_grade": "<50",        "sleep": "5-6 hrs",
        "expected": "Poor"
    },
    {
        "name": "Lalita Devi",      "age": 18, "absences": 12,
        "study": "1-2 hrs",         "consistency": "Rarely",
        "assignment": "Low",        "participation": "Low",
        "prev_grade": "<50",        "sleep": "<5 hrs",
        "expected": "Poor"
    },
    {
        "name": "Nikhil Rao",       "age": 21, "absences": 14,
        "study": "<1 hr",           "consistency": "Sometimes",
        "assignment": "Low",        "participation": "Low",
        "prev_grade": "<50",        "sleep": "5-6 hrs",
        "expected": "Poor"
    },

    # --- AVERAGE (5 cases) ---
    {
        "name": "Sneha Sharma",     "age": 20, "absences": 4,
        "study": "2-4 hrs",         "consistency": "Regular",
        "assignment": "Medium",     "participation": "Moderate",
        "prev_grade": "50-60",      "sleep": "6-7 hrs",
        "expected": "Average"
    },
    {
        "name": "Rohit Verma",      "age": 19, "absences": 8,
        "study": "1-2 hrs",         "consistency": "Sometimes",
        "assignment": "Medium",     "participation": "Moderate",
        "prev_grade": "50-60",      "sleep": "5-6 hrs",
        "expected": "Average"
    },
    {
        "name": "Divya Menon",      "age": 20, "absences": 6,
        "study": "1-2 hrs",         "consistency": "Regular",
        "assignment": "Medium",     "participation": "Moderate",
        "prev_grade": "50-60",      "sleep": "6-7 hrs",
        "expected": "Average"
    },
    {
        "name": "Arun Pillai",      "age": 22, "absences": 5,
        "study": "2-4 hrs",         "consistency": "Sometimes",
        "assignment": "Medium",     "participation": "Low",
        "prev_grade": "50-60",      "sleep": "5-6 hrs",
        "expected": "Average"
    },
    {
        "name": "Meera Iyer",       "age": 19, "absences": 7,
        "study": "2-4 hrs",         "consistency": "Regular",
        "assignment": "Medium",     "participation": "Moderate",
        "prev_grade": "50-60",      "sleep": "6-7 hrs",
        "expected": "Average"
    },

    # --- GOOD (5 cases) ---
    {
        "name": "Karan Mehta",      "age": 21, "absences": 2,
        "study": "4-6 hrs",         "consistency": "Regular",
        "assignment": "High",       "participation": "High",
        "prev_grade": "60-75",      "sleep": ">7 hrs",
        "expected": "Good"
    },
    {
        "name": "Fatima Sheikh",    "age": 20, "absences": 1,
        "study": "2-4 hrs",         "consistency": "Very Regular",
        "assignment": "High",       "participation": "High",
        "prev_grade": "60-75",      "sleep": ">7 hrs",
        "expected": "Good"
    },
    {
        "name": "Arjun Nambiar",    "age": 21, "absences": 3,
        "study": "4-6 hrs",         "consistency": "Regular",
        "assignment": "High",       "participation": "Moderate",
        "prev_grade": "60-75",      "sleep": "6-7 hrs",
        "expected": "Good"
    },
    {
        "name": "Pooja Krishnan",   "age": 22, "absences": 2,
        "study": "4-6 hrs",         "consistency": "Very Regular",
        "assignment": "High",       "participation": "High",
        "prev_grade": "60-75",      "sleep": ">7 hrs",
        "expected": "Good"
    },
    {
        "name": "Sameer Joshi",     "age": 20, "absences": 1,
        "study": "2-4 hrs",         "consistency": "Regular",
        "assignment": "High",       "participation": "High",
        "prev_grade": "60-75",      "sleep": "6-7 hrs",
        "expected": "Good"
    },

    # --- EXCELLENT (5 cases) ---
    {
        "name": "Ananya Singh",     "age": 21, "absences": 0,
        "study": ">6 hrs",          "consistency": "Very Regular",
        "assignment": "Very High",  "participation": "High",
        "prev_grade": ">75",        "sleep": ">7 hrs",
        "expected": "Excellent"
    },
    {
        "name": "Vikram Reddy",     "age": 22, "absences": 0,
        "study": ">6 hrs",          "consistency": "Very Regular",
        "assignment": "Very High",  "participation": "High",
        "prev_grade": ">75",        "sleep": ">7 hrs",
        "expected": "Excellent"
    },
    {
        "name": "Kavya Nair",       "age": 20, "absences": 0,
        "study": "4-6 hrs",         "consistency": "Very Regular",
        "assignment": "Very High",  "participation": "High",
        "prev_grade": ">75",        "sleep": ">7 hrs",
        "expected": "Excellent"
    },
    {
        "name": "Ishaan Gupta",     "age": 21, "absences": 1,
        "study": ">6 hrs",          "consistency": "Very Regular",
        "assignment": "Very High",  "participation": "High",
        "prev_grade": ">75",        "sleep": ">7 hrs",
        "expected": "Excellent"
    },
    {
        "name": "Zara Hussain",     "age": 19, "absences": 0,
        "study": ">6 hrs",          "consistency": "Very Regular",
        "assignment": "Very High",  "participation": "High",
        "prev_grade": ">75",        "sleep": ">7 hrs",
        "expected": "Excellent"
    },
]

results = []


async def wait(page, ms=1500):
    await page.wait_for_timeout(ms)


async def select_streamlit_dropdown(page, label, value):
    """
    Clicks a Streamlit custom dropdown by label and selects the option by text.
    Streamlit dropdowns are NOT native <select> — they are custom divs.
    """
    try:
        dropdown = page.locator('[data-testid="stSelectbox"]').filter(
            has=page.locator('label', has_text=label)
        ).first
        await dropdown.click()
        await wait(page, 600)
        option = page.locator('[data-testid="stSelectboxVirtualDropdown"] li').filter(
            has_text=value
        ).first
        await option.click()
        await wait(page, 500)
    except Exception as e:
        print(f"  ⚠️  Dropdown '{label}' → '{value}': {e}")


async def set_number(page, label, value):
    try:
        field = page.get_by_role("spinbutton", name=label)
        await field.click()
        await page.keyboard.press("Control+A")
        await page.keyboard.type(str(value))
        await wait(page, 400)
    except Exception as e:
        print(f"  ⚠️  Number field '{label}': {e}")


async def login(page):
    print("🔐 Logging in...")
    await page.goto(APP_URL)
    await wait(page, 4000)
    await page.get_by_placeholder("Enter your username").fill(ADMIN_USER)
    await wait(page, 300)
    await page.get_by_placeholder("Enter password").fill(ADMIN_PASS)
    await wait(page, 300)
    await page.get_by_role("button", name="Login").click()
    await wait(page, 3000)
    print("✅ Logged in\n")


async def submit_student(page, student):
    print(f"📋 {student['name']} (Expected: {student['expected']})")

    await page.get_by_label("Student Name").fill(student["name"])
    await wait(page, 400)

    await set_number(page, "Age", student["age"])
    await set_number(page, "Monthly Absences", student["absences"])

    await select_streamlit_dropdown(page, "Daily Study Time",           student["study"])
    await select_streamlit_dropdown(page, "Study Consistency",          student["consistency"])
    await select_streamlit_dropdown(page, "Assignment Completion Rate", student["assignment"])
    await select_streamlit_dropdown(page, "Class Participation",        student["participation"])
    await select_streamlit_dropdown(page, "Previous Semester Average",  student["prev_grade"])
    await select_streamlit_dropdown(page, "Sleep Duration",             student["sleep"])

    await page.get_by_role("button", name="Predict Performance").click()
    await wait(page, 2500)

    try:
        # Try multiple locator strategies to find the result
        result_text = None
        for locator in [
            page.get_by_text("Predicted Performance:", exact=False),
            page.locator("[data-testid=stSuccess]"),
            page.locator(".stAlert"),
            page.locator("div").filter(has_text="Predicted Performance:").last,
        ]:
            try:
                await locator.wait_for(timeout=5000)
                result_text = await locator.inner_text()
                if "Predicted Performance:" in result_text:
                    break
            except Exception:
                continue

        if result_text and "Predicted Performance:" in result_text:
            prediction = result_text.replace("Predicted Performance:", "").strip()
            match = "✅" if prediction == student["expected"] else "❌"
            print(f"  {match} Got: {prediction} | Expected: {student['expected']}")
            results.append({"Name": student["name"], "Expected": student["expected"], "Got": prediction, "Match": prediction == student["expected"]})
        else:
            print(f"  ⚠️  Could not find result text")
            results.append({"Name": student["name"], "Expected": student["expected"], "Got": "NOT FOUND", "Match": False})
    except Exception as e:
        print(f"  ⚠️  Could not read result: {e}")
        results.append({"Name": student["name"], "Expected": student["expected"], "Got": "ERROR", "Match": False})

    # Reset form for next student
    try:
        reset_btn = page.get_by_role("button", name="Predict Another Student")
        await reset_btn.scroll_into_view_if_needed()
        await wait(page, 500)
        await reset_btn.click()
        await wait(page, 3000)
        print("  🔄 Form reset")
    except Exception as e:
        print(f"  ⚠️  Reset failed: {e} — reloading page")
        await page.reload()
        await wait(page, 4000)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await login(page)
        for student in test_students:
            await submit_student(page, student)
            print()
        # Keep browser open for review
        print("👀 Browser staying open for review. Press Enter to close...")
        input()
        await browser.close()

    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    passed = sum(1 for r in results if r["Match"])
    for r in results:
        icon = "✅" if r["Match"] else "❌"
        print(f"  {icon} {r['Name']}: Expected {r['Expected']}, Got {r['Got']}")
    print(f"\n  Passed: {passed}/{len(results)}")
    print("="*50)


asyncio.run(main())