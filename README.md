Here's a clean and well-structured **Markdown document** explaining the data flow 

# 🧠 Model Data Flow Documentation

## 📥 1. User Input Fields

These values are taken from the form submitted by the user via `POST`:

| Field Name       | Data Type | Description |
|------------------|-----------|-------------|
| `batting_team`   | `str`     | Name of the team currently batting |
| `bowling_team`   | `str`     | Name of the team currently bowling |
| `selected_city`  | `str`     | City where the match is being played |
| `target`         | `int`     | Total runs required to win (Target score) |
| `score`          | `int`     | Current score of the batting team |
| `balls_left`     | `int`     | Balls remaining in the innings |
| `wickets`        | `int`     | Number of wickets lost so far |

---

## 🧮 2. Derived Features (Calculated in Backend)

These features are calculated using the user input:

| Feature Name         | Formula / Logic |
|----------------------|------------------|
| `runs_left`          | `target - score` |
| `wickets_remaining`  | `10 - wickets` |
| `overs_completed`    | `(120 - balls_left) / 6` *(20 overs = 120 balls)* |
| `crr` (Current Run Rate) | `score / overs_completed` |
| `rrr` (Required Run Rate) | `runs_left / (balls_left / 6)` |

---

## 📦 3. Final Model Input DataFrame

This is the full DataFrame passed to the model (`pipe.predict_proba()`):

| Column Name        | Source              | Description |
|--------------------|---------------------|-------------|
| `batting_team`     | User input          | Categorical |
| `bowling_team`     | User input          | Categorical |
| `city`             | User input          | Categorical |
| `runs_left`        | Derived             | Target - Score |
| `balls_left`       | User input          | Balls remaining |
| `wickets_remaining`| Derived             | 10 - Wickets |
| `total_run_x`      | User input (`target`)| Used in training as total runs |
| `crr`              | Derived             | Current run rate |
| `rrr`              | Derived             | Required run rate |

---

## 🧾 4. Model Output

- The model returns probabilities via `predict_proba()`.
- Output:  
  - `result[0][1]` = Probability of winning  
  - `result[0][0]` = Probability of losing  

These are then rounded and rendered to `result.html` as:

- `win_probability`
- `loss_probability`

---

