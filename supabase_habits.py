"""
Supabase integration for Habit Tracker.

SETUP STEPS:
1. Go to https://supabase.com -> create a free project.
2. In the SQL Editor, run the schema below to create your tables.
3. Get your Project URL and anon/public API key from Settings > API.
4. pip install supabase
5. Store credentials in .streamlit/secrets.toml (NEVER hardcode them):

    [supabase]
    url = "https://YOUR_PROJECT.supabase.co"
    key = "YOUR_ANON_KEY"

--------------------------------------------------------------------
SQL SCHEMA (run once in Supabase SQL Editor):
--------------------------------------------------------------------

create table habits (
    id bigint generated always as identity primary key,
    user_id text not null default 'default_user',   -- swap for real auth later
    name text not null,
    goal int not null default 0,                     -- e.g. target check-ins per month
    created_at timestamp with time zone default now()
);

create table checkins (
    id bigint generated always as identity primary key,
    habit_id bigint references habits(id) on delete cascade,
    user_id text not null default 'default_user',
    checkin_date date not null,
    completed boolean not null default true,
    created_at timestamp with time zone default now(),
    unique (habit_id, checkin_date)   -- one entry per habit per day
);

-- Recommended: enable Row Level Security once you add real auth
-- alter table habits enable row level security;
-- alter table checkins enable row level security;

--------------------------------------------------------------------
"""

import streamlit as st
from supabase import create_client, Client
from datetime import date


@st.cache_resource
def get_supabase_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


# ---------- Habits ----------

def add_habit(name: str, goal: int = 0, user_id: str = "default_user"):
    sb = get_supabase_client()
    return sb.table("habits").insert(
        {"name": name, "goal": goal, "user_id": user_id}
    ).execute()


def get_habits(user_id: str = "default_user"):
    sb = get_supabase_client()
    res = sb.table("habits").select("*").eq("user_id", user_id).execute()
    return res.data


def delete_habit(habit_id: int):
    sb = get_supabase_client()
    return sb.table("habits").delete().eq("id", habit_id).execute()


# ---------- Check-ins ----------

def mark_checkin(habit_id: int, checkin_date: date = None,
                  completed: bool = True, user_id: str = "default_user"):
    sb = get_supabase_client()
    checkin_date = checkin_date or date.today()
    # upsert: overwrite if a check-in for that habit+date already exists
    return sb.table("checkins").upsert(
        {
            "habit_id": habit_id,
            "user_id": user_id,
            "checkin_date": str(checkin_date),
            "completed": completed,
        },
        on_conflict="habit_id,checkin_date",
    ).execute()


def get_checkins(habit_id: int = None, user_id: str = "default_user"):
    sb = get_supabase_client()
    q = sb.table("checkins").select("*").eq("user_id", user_id)
    if habit_id is not None:
        q = q.eq("habit_id", habit_id)
    return q.execute().data


def get_checkins_for_month(year: int, month: int, user_id: str = "default_user"):
    sb = get_supabase_client()
    start = f"{year}-{month:02d}-01"
    end_month = month + 1 if month < 12 else 1
    end_year = year if month < 12 else year + 1
    end = f"{end_year}-{end_month:02d}-01"
    res = (
        sb.table("checkins")
        .select("*")
        .eq("user_id", user_id)
        .gte("checkin_date", start)
        .lt("checkin_date", end)
        .execute()
    )
    return res.data
