def create_execution_report(results):

    total_records = len(results)

    success_count = 0
    failed_count = 0

    for result in results:

        if result["status"] == "success":
            success_count += 1
        else:
            failed_count += 1

    return {
        "total_records": total_records,
        "success_count": success_count,
        "failed_count": failed_count,
        "results": results
    }
