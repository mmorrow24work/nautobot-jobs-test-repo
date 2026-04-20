import csv
from io import StringIO

from django.core.exceptions import ValidationError, ObjectDoesNotExist

from nautobot.extras.jobs import Job, FileVar
from nautobot.dcim.models import Device, DeviceType, Location
from nautobot.extras.models import Status, Role

name = "Jobs Collection nautobot-jobs-test-repo"

class FileUpload_3(Job):
    class Meta:
        name = "CSV File Upload and Process"
        description = "Please select a CSV file for upload"

    file = FileVar(description="CSV File to upload")

    def run(self, file):
        file_contents = file.read().decode("utf-8", errors="replace")

        # Use csv reader for robust parsing
        reader = csv.DictReader(StringIO(file_contents))

        # Cache commonly used objects
        try:
            active_status = Status.objects.get(name="Active")
        except Status.DoesNotExist:
            raise RuntimeError("Status 'Active' not found in Nautobot.")

        created = 0
        skipped_existing = 0
        failed = 0

        for row_num, row in enumerate(reader, start=2):  # start=2 because header is line 1
            try:
                device_name = (row.get("device_name") or row.get("name") or "").strip()
                role_name = (row.get("role_name") or row.get("role") or "").strip()
                model_name = (row.get("model_name") or row.get("model") or "").strip()
                location_name = (row.get("location_name") or row.get("location") or "").strip()

                if not all([device_name, role_name, model_name, location_name]):
                    self.logger.warning(f"Row {row_num}: Missing required fields: {row}. Skipping.")
                    failed += 1
                    continue

                # Lookups
                role = Role.objects.get(name=role_name)
                device_type = DeviceType.objects.get(model=model_name)
                location = Location.objects.get(name=location_name)

                # Optional: fast pre-check to avoid hitting validated_save() validation
                # Since your uniqueness is location+tenant+name, and your tenant is None:
                if Device.objects.filter(name=device_name, location=location, tenant__isnull=True).exists():
                    self.logger.warning(
                        f"Row {row_num}: Device '{device_name}' already exists in location '{location_name}' "
                        f"(tenant=None). Skipping."
                    )
                    skipped_existing += 1
                    continue

                device = Device(
                    name=device_name,
                    device_type=device_type,
                    location=location,
                    status=active_status,
                    role=role,
                )

                device.validated_save()
                created += 1
                self.logger.info(f"Row {row_num}: Created device '{device_name}'.")

            except ObjectDoesNotExist as e:
                self.logger.error(f"Row {row_num}: Lookup failed ({e}). Row data: {row}")
                failed += 1

            except ValidationError as e:
                # If some other validation fails, log error and continue
                self.logger.error(f"Row {row_num}: Validation error for '{row}': {e}")
                failed += 1

            except Exception as e:
                self.logger.exception(f"Row {row_num}: Unexpected error for '{row}': {e}")
                failed += 1

        return (
            f"Execution completed. Created={created}, SkippedExisting={skipped_existing}, Failed={failed}"
        )
