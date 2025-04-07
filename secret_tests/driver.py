import importlib.util
import os
import datetime
import inspect
import random
import string

def test_student_code(solution_path):
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "report.txt"))
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    if os.path.exists(report_path):
        os.remove(report_path)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)

    results = []

    if not hasattr(student_module, 'FitnessTracker'):
        results.append("❌ TC1: Registering a New Fitness User failed | Reason: FitnessTracker class missing")
        write_report(report_path, results)
        return

    tracker = student_module.FitnessTracker()

    # Define the expected method signatures (WITHOUT the 'self' parameter)
    expected_signatures = {
        "register_user": ["fitness_data", "user_name"],
        "log_workout": ["fitness_data", "user_name", "calories_burned"],
        "calculate_average_calories": ["fitness_data", "user_name"],
        "generate_progress_report": ["fitness_data"]
    }

    signature_failures = []
    for method, expected_params in expected_signatures.items():
        if not hasattr(tracker, method):
            signature_failures.append(f"{method} (method missing)")
        else:
            actual_params = list(inspect.signature(getattr(tracker, method)).parameters.keys())
            if actual_params != expected_params:
                signature_failures.append(f"{method} (expected {expected_params}, got {actual_params})")

    # Generate random test data to combat hardcoding
    def random_username():
        # Generate a random username that's not "Alice" or "Bob"
        while True:
            name = ''.join(random.choice(string.ascii_uppercase) for _ in range(1)) + \
                   ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
            if name not in ["Alice", "Bob"]:
                return name
    
    # Anti-cheat strategy: Use different random usernames for each test
    test_user1 = random_username()
    test_user2 = random_username()
    test_user3 = random_username()
    
    # Random calorie values
    calories1 = random.randint(100, 500)
    calories2 = random.randint(100, 500)
    
    # Run each test independently
    # TC1: Test register_user
    try:
        if any(failure.startswith("register_user") for failure in signature_failures):
            raise TypeError(f"Signature mismatch for register_user: {next(f for f in signature_failures if f.startswith('register_user'))}")
        
        # Create a fresh data dictionary for this test
        data = {}
        
        # First test
        res = tracker.register_user(data, test_user1)
        
        # Check if the result has the correct structure - look for the random username
        if isinstance(res, dict) and test_user1 in res and \
           isinstance(res[test_user1], dict) and \
           res[test_user1].get("workouts") == 0 and \
           res[test_user1].get("calories") == 0 and \
           res[test_user1].get("status") == "Inactive":
            
            # Anti-cheat: Make sure the function modifies the input dictionary correctly
            # and doesn't just return a hardcoded dictionary
            if test_user1 in data and data[test_user1].get("workouts") == 0:
                # Second test with a different username to detect hardcoding
                data2 = {}
                res2 = tracker.register_user(data2, test_user2)
                
                if test_user2 in res2 and test_user2 in data2:
                    results.append("✅ TC1: Registering a New Fitness User")
                else:
                    results.append(f"❌ TC1: Registering a New Fitness User failed | Reason: Doesn't handle different usernames correctly")
            else:
                results.append(f"❌ TC1: Registering a New Fitness User failed | Reason: Function doesn't modify the input dictionary correctly")
        else:
            results.append(f"❌ TC1: Registering a New Fitness User failed | Reason: Incorrect structure. Expected {{'{test_user1}': {{'workouts': 0, 'calories': 0, 'status': 'Inactive'}}}} but got {res}")
    except Exception as e:
        results.append(f"❌ TC1: Registering a New Fitness User failed | Reason: {str(e)}")

    # TC2: Test log_workout
    try:
        if any(failure.startswith("log_workout") for failure in signature_failures):
            raise TypeError(f"Signature mismatch for log_workout: {next(f for f in signature_failures if f.startswith('log_workout'))}")
        
        # Create a fresh data dictionary for this test
        data = {test_user1: {'workouts': 0, 'calories': 0, 'status': 'Inactive'}}
        
        # Log a workout with random calories amount
        res = tracker.log_workout(data, test_user1, calories1)
        
        if isinstance(res, dict) and test_user1 in res and \
           res[test_user1].get("workouts") == 1 and \
           res[test_user1].get("calories") == calories1:
            
            # Anti-cheat: Test with different calorie value
            data = {test_user2: {'workouts': 0, 'calories': 0, 'status': 'Inactive'}}
            res2 = tracker.log_workout(data, test_user2, calories2)
            
            if test_user2 in res2 and \
               res2[test_user2].get("workouts") == 1 and \
               res2[test_user2].get("calories") == calories2:
                results.append("✅ TC2: Logging a Workout Session")
            else:
                results.append(f"❌ TC2: Logging a Workout Session failed | Reason: Doesn't handle different calorie values correctly")
        else:
            results.append(f"❌ TC2: Logging a Workout Session failed | Reason: Incorrect update. Expected workouts=1, calories={calories1} but got {res.get(test_user1, {})}")
    except Exception as e:
        results.append(f"❌ TC2: Logging a Workout Session failed | Reason: {str(e)}")

    # TC3: Test calculate_average_calories
    try:
        if any(failure.startswith("calculate_average_calories") for failure in signature_failures):
            raise TypeError(f"Signature mismatch for calculate_average_calories: {next(f for f in signature_failures if f.startswith('calculate_average_calories'))}")
        
        # Create a fresh data dictionary for this test with random values
        workout_count = random.randint(2, 5)
        total_calories = random.randint(500, 1000)
        expected_avg = total_calories / workout_count
        
        data = {test_user3: {'workouts': workout_count, 'calories': total_calories, 'status': 'Inactive'}}
        avg = tracker.calculate_average_calories(data, test_user3)
        
        if isinstance(avg, (int, float)) and abs(avg - expected_avg) < 0.01:
            # Anti-cheat: Test with a different set of values
            workout_count2 = random.randint(2, 5)
            total_calories2 = random.randint(500, 1000)
            expected_avg2 = total_calories2 / workout_count2
            
            data2 = {test_user2: {'workouts': workout_count2, 'calories': total_calories2, 'status': 'Inactive'}}
            avg2 = tracker.calculate_average_calories(data2, test_user2)
            
            if abs(avg2 - expected_avg2) < 0.01:
                results.append("✅ TC3: Calculating Average Calories Burned")
            else:
                results.append(f"❌ TC3: Calculating Average Calories Burned failed | Reason: Doesn't calculate different values correctly")
        else:
            results.append(f"❌ TC3: Calculating Average Calories Burned failed | Reason: Incorrect average. Expected {expected_avg} but got {avg}")
    except Exception as e:
        results.append(f"❌ TC3: Calculating Average Calories Burned failed | Reason: {str(e)}")

    # HTC1: Test generate_progress_report
    try:
        if any(failure.startswith("generate_progress_report") for failure in signature_failures):
            raise TypeError(f"Signature mismatch for generate_progress_report: {next(f for f in signature_failures if f.startswith('generate_progress_report'))}")
        
        # Test with 3 different users with different calorie levels to detect hardcoding
        # Beginner: less than 1000
        # Intermediate: 1000-5000
        # Advanced: over 5000
        data = {
            f"{test_user1}": {'workouts': 3, 'calories': 800, 'status': 'Inactive'},
            f"{test_user2}": {'workouts': 5, 'calories': 3000, 'status': 'Active'},
            f"{test_user3}": {'workouts': 10, 'calories': 6000, 'status': 'Active'}
        }
        
        report = tracker.generate_progress_report(data)
        
        if isinstance(report, dict) and \
           report.get(test_user1) == "Beginner" and \
           report.get(test_user2) == "Intermediate" and \
           report.get(test_user3) == "Advanced":
            results.append("✅ HTC1: Generating Progress Reports")
        else:
            results.append(f"❌ HTC1: Generating Progress Reports failed | Reason: Incorrect classification. Expected {{'{test_user1}': 'Beginner', '{test_user2}': 'Intermediate', '{test_user3}': 'Advanced'}} but got {report}")
    except Exception as e:
        results.append(f"❌ HTC1: Generating Progress Reports failed | Reason: {str(e)}")

    # HTC2: Test error handling for non-existent users
    try:
        if any(failure.startswith("log_workout") for failure in signature_failures):
            raise TypeError(f"Signature mismatch for log_workout: {next(f for f in signature_failures if f.startswith('log_workout'))}")
        
        # Create a fresh data dictionary for this test
        nonexistent_user = "NonExistentUser_" + ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
        data = {}
        
        # This should raise an exception since the user doesn't exist
        tracker.log_workout(data, nonexistent_user, 200)
        
        # If we get here, no exception was raised
        results.append("❌ HTC2: Handling Workout Logging for Non-Existent Users failed | Reason: Expected exception for non-existent user")
    except Exception:
        # We expect an exception here
        results.append("✅ HTC2: Handling Workout Logging for Non-Existent Users")

    print("\n".join(results))
    write_report(report_path, results)

def write_report(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "solution.py"))
    test_student_code(path)