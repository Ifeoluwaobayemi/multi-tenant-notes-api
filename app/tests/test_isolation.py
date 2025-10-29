import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_cross_tenant_isolation(client: AsyncClient):
    # create org A
    res_a = await client.post("/organizations/", json={"name": "OrgA"})
    org_a = res_a.json()
    org_a_id = org_a["id"]

    # create org B
    res_b = await client.post("/organizations/", json={"name": "OrgB"})
    org_b = res_b.json()
    org_b_id = org_b["id"]

    pw = "secret"

    # create writer in org A
    await client.post(f"/organizations/{org_a_id}/users/", json={"username":"writerA","password":pw,"role":"writer"})
    res_token_a = await client.post(f"/organizations/{org_a_id}/users/login", json={"username":"writerA","password":pw})
    token_a = res_token_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # writer in org A creates a note
    res_note = await client.post("/notes/", json={"title":"A note","content":"for A"}, headers=headers_a)
    assert res_note.status_code == 201
    note_id = res_note.json()["id"]

    # create reader in org B
    await client.post(f"/organizations/{org_b_id}/users/", json={"username":"readerB","password":pw,"role":"reader"})
    res_token_b = await client.post(f"/organizations/{org_b_id}/users/login", json={"username":"readerB","password":pw})
    token_b = res_token_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # reader from org B should not retrieve org A's note
    res_get = await client.get(f"/notes/{note_id}", headers=headers_b)
    assert res_get.status_code == 404
