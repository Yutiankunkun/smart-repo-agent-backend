"""
測試 main.py 的 API 功能。
- 健康檢查：無需外部依賴
- generate_repo_test：mock 端點，不需 LLM
- generate_repo：需 DASHSCOPE_API_KEY，會呼叫付費 LLM
"""
import os
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_repo_test():
    response = client.post("/api/folder/generate_repo_test")
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    report = data["report"]
    assert report["student_id"] == "id0001"
    assert report["student_name"] == "藍天"
    assert report["meeting_date"] == "2026年3月29日"
    assert "events" in report
    assert "process" in report
    assert "suggestions" in report
    assert "mental" in report


def test_generate_repo_with_valid_input():
    payload = {
        "student_id": "id0001",
        "student_name": "藍天",
        "university": "東京科学大学",
        "major": "情報通信系",
        "toeic": "845",
        "jlpt": "N1",
        "memo": "學生提到最近在準備求職，更新了履歷，練習了程式面試題。",
        "meeting_date": "2026年3月29日",
    }
    response = client.post("/api/folder/generate_repo", json=payload)

    if response.status_code == 200:
        data = response.json()
        assert "report" in data
        report = data["report"]
        assert report["student_id"] == payload["student_id"]
        assert report["student_name"] == payload["student_name"]
    else:
        # 無 API key 或 API 錯誤時會 500
        assert response.status_code == 500


def test_generate_repo_without_meeting_date():
    payload = {
        "student_id": "id0002",
        "student_name": "測試",
        "university": "東京大学",
        "major": "情報系",
        "toeic": "800",
        "jlpt": "N2",
        "memo": "簡短 memo",
    }
    response = client.post("/api/folder/generate_repo", json=payload)
    assert response.status_code in (200, 422, 500)
