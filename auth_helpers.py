"""
Supabase data access for Habit Tracker.

NOTE: user_id is intentionally NOT passed on inserts -- the `habits` and
`checkins` tables default that column to auth.uid(), and Row Level
Security policies ensure each logged-in user only ever sees their own
rows. See auth_helpers.py for the login/session handling and
supabase_auth_migration.sql for the schema + RLS policies.
"""

from datetime import date
from auth_helpers import get_supabase_client


# ---------- Habits ----------

def add_habit(name: str, goal: int = 0):
    sb = get_supabase_client()
    return sb.table("habits").insert({"name": name, "goal": goal}).execute()


def get_habits():
    sb = get_supabase_client()
    # RLS automatically restricts this to the logged-in user's rows
    res = sb.table("habits").select("*").execute()
    return res.data


def delete_habit(habit_id: int):
    sb = get_supabase_client()
    return sb.table("habits").delete().eq("id", habit_id).execute()


def update_habit_goal(habit_id: int, goal: int):
    sb = get_supabase_client()
    return sb.table("habits").update({"goal": goal}).eq("id", habit_id).execute()


# ---------- Check-ins ----------

def mark_checkin(habit_id: int, checkin_date: date = None, completed: bool = True):
    sb = get_supabase_client()
    checkin_date = checkin_date or date.today()
    return sb.table("checkins").upsert(
        {
            "habit_id": habit_id,
            "checkin_date": str(checkin_date),
            "completed": completed,
        },
        on_conflict="habit_id,checkin_date",
    ).execute()


def get_checkins(habit_id: int = None):
    sb = get_supabase_client()
    q = sb.table("checkins").select("*")
    if habit_id is not None:
        q = q.eq("habit_id", habit_id)
    return q.execute().data


def get_checkins_for_month(year: int, month: int):
    sb = get_supabase_client()
    start = f"{year}-{month:02d}-01"
    end_month = month + 1 if month < 12 else 1
    end_year = year if month < 12 else year + 1
    end = f"{end_year}-{end_month:02d}-01"
    res = (
        sb.table("checkins")
        .select("*")
        .gte("checkin_date", start)
        .lt("checkin_date", end)
        .execute()
    )
    return res.data
