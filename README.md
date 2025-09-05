# ChatBotMessageCount-fastAPI
Keeps count of users chat messages with LLM, keeps track of the count and stops user at specified amount and resets at also specified hours.
# 💬 FastAPI Chat Message Limiter

A **FastAPI backend service** that tracks how many chat messages each user sends, enforces a **usage limit**, and automatically **resets their quota** after a given time window.  

This project is useful for:
- Preventing free users from spamming your chatbot
- Encouraging upgrades to a paid plan once limits are reached
- Keeping your API cost-effective by enforcing message quotas

---

## ✨ Features

- 🔐 **User-based tracking** — each user has their own message counter.
- ⏳ **Quota enforcement** — stops users after `N` messages within a defined window.
- ♻️ **Automatic reset** — quotas reset after a configurable time period.
- 🛠 **Database-backed** — persistent counters stored in Postgres (or any SQLAlchemy-compatible DB).
- ⚡ **FastAPI + SQLAlchemy** — async, modern, and scalable backend.

---

## 🏗️ Project Structure

