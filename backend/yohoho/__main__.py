import uvicorn

if __name__ == "__main__":
    uvicorn.run("yohoho.app:create_app", factory=True, host="0.0.0.0", port=5000, reload=True)
