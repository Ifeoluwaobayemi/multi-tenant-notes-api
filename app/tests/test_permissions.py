import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_rbac_flow(client: AsyncClient):
    # create org via route
    res_org = await client.post("/organizations/", json={"name": "TestOrg"})
    assert res_org.status_code == 201
    org = res_org.json()
    org_id = org["id"]

    # create users
    pw = "secret123"
    res_w = await client.post(f"/organizations/{org_id}/users/", json={"username":"writer1","password":pw,"role":"writer"})
    assert res_w.status_code == 201
    res_r = await client.post(f"/organizations/{org_id}/users/", json={"username":"reader1","password":pw,"role":"reader"})
    assert res_r.status_code == 201
    res_a = await client.post(f"/organizations/{org_id}/users/", json={"username":"admin1","password":pw,"role":"admin"})
    assert res_a.status_code == 201

    # login writer
    res_token_w = await client.post(f"/organizations/{org_id}/users/login", json={"username":"writer1","password":pw})
    assert res_token_w.status_code == status.HTTP_200_OK
    token_w = res_token_w.json()["access_token"]
    headers_w = {"Authorization": f"Bearer {token_w}"}

    # writer creates note
    res_note = await client.post("/notes/", json={"title":"Hello","content":"World"}, headers=headers_w)
    assert res_note.status_code == 201
    note_id = res_note.json()["id"]

    # reader login & attempt create
    res_token_r = await client.post(f"/organizations/{org_id}/users/login", json={"username":"reader1","password":pw})
    token_r = res_token_r.json()["access_token"]
    headers_r = {"Authorization": f"Bearer {token_r}"}
    res_fail_create = await client.post("/notes/", json={"title":"X","content":"Y"}, headers=headers_r)
    assert res_fail_create.status_code == status.HTTP_403_FORBIDDEN

    # admin delete
    res_token_a = await client.post(f"/organizations/{org_id}/users/login", json={"username":"admin1","password":pw})
    token_a = res_token_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    res_del = await client.delete(f"/notes/{note_id}", headers=headers_a)
    assert res_del.status_code == status.HTTP_204_NO_CONTENT
