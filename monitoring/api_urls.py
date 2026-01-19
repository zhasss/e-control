from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    RegionViewSet,
    DistrictViewSet,
    SchoolViewSet,
    InspectionTypeViewSet,
    CriterionCategoryViewSet,
    CriterionViewSet,
    InspectionViewSet,
    InspectionResultViewSet,
    MeView,  # <-- добавили
)

router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"districts", DistrictViewSet, basename="district")
router.register(r"schools", SchoolViewSet, basename="school")
router.register(r"inspection-types", InspectionTypeViewSet, basename="inspection-type")
router.register(r"criterion-categories", CriterionCategoryViewSet, basename="criterion-category")
router.register(r"criterions", CriterionViewSet, basename="criterion")
router.register(r"inspections", InspectionViewSet, basename="inspection")
router.register(r"inspection-results", InspectionResultViewSet, basename="inspection-result")

urlpatterns = [
    path("me/", MeView.as_view(), name="monitoring-me"),
    path("", include(router.urls)),
]
