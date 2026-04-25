from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LyraModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class BilingualText(LyraModel):
    en: str
    zh: str


class RoutePageSummary(LyraModel):
    routePageId: str
    slug: str
    title: BilingualText
    subtitle: BilingualText
    price: int
    image: str
    highlights: list[str] = Field(default_factory=list)
    duration: int
    group: int | None = None
    status: str


class RoutePageQueryResponse(LyraModel):
    route_id: str
    summary: RoutePageSummary | None = None


class RoutePageListResponse(LyraModel):
    items: list[RoutePageSummary]


class RoutePageJourneyHeroMetrics(LyraModel):
    durationDays: int
    basePriceUsd: int
    groupSize: int
    rating: int | float


class RoutePageJourneyHero(LyraModel):
    title: BilingualText
    subtitle: BilingualText | None = None
    tags: list[BilingualText] = Field(default_factory=list)
    metrics: RoutePageJourneyHeroMetrics


class RoutePageJourneyImage(LyraModel):
    src: str
    alt: BilingualText | None = None


class RoutePageJourneyCityHighlight(LyraModel):
    city_id: str
    city_name: BilingualText
    city_subtitle: BilingualText | None = None
    days: int | None = None
    image: str | None = None
    map_coords: dict[str, int] | None = None


class RoutePageJourney(LyraModel):
    routePageId: str
    hero: RoutePageJourneyHero
    selling_points: list[BilingualText] = Field(default_factory=list)
    map_image: RoutePageJourneyImage | None = None
    city_highlights: list[RoutePageJourneyCityHighlight] = Field(default_factory=list)


class RoutePageItineraryThemeCity(LyraModel):
    city_id: str
    city_name: BilingualText
    days: int | None = None
    city_subtitle: BilingualText | None = None
    city_rec: BilingualText | None = None
    city_guide: BilingualText
    transports: BilingualText | None = None
    transmodel: str | None = None
    imgs: list[RoutePageJourneyImage] = Field(default_factory=list)


class RoutePageItineraryTheme(LyraModel):
    id: str
    title: BilingualText
    subtitle: BilingualText
    days: int | None = None
    cities: list[RoutePageItineraryThemeCity] = Field(default_factory=list)


class RoutePageItinerary(LyraModel):
    routePageId: str
    themes: list[RoutePageItineraryTheme] = Field(default_factory=list)


class RoutePageHotelItem(LyraModel):
    name: BilingualText
    city: BilingualText | None = None
    location: BilingualText | None = None
    nights: int | None = None
    description: BilingualText | None = None
    image: str | None = None
    featured: bool = False


class RoutePageHotels(LyraModel):
    routePageId: str
    items: list[RoutePageHotelItem] = Field(default_factory=list)


class RoutePageExperienceHost(LyraModel):
    name: BilingualText
    role: BilingualText | None = None
    bio: BilingualText | None = None
    avatarLabel: str | None = None


class RoutePageExperienceItem(LyraModel):
    city: BilingualText | None = None
    tag: BilingualText | None = None
    image: str | None = None
    title: BilingualText
    subtitle: BilingualText | None = None
    description: BilingualText | None = None
    exclusiveAccess: BilingualText | None = None
    host: RoutePageExperienceHost | None = None


class RoutePageExperiences(LyraModel):
    routePageId: str
    subheadline: BilingualText | None = None
    items: list[RoutePageExperienceItem] = Field(default_factory=list)


class RoutePageConciergeStat(LyraModel):
    n: str
    label: str


class RoutePageConcierge(LyraModel):
    routePageId: str
    id: str
    name: str
    avatarInitials: str | None = None
    title: str
    tagline: str | None = None
    bio: str | None = None
    stats: list[RoutePageConciergeStat] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    isOnline: bool | None = None
    onlineLabel: str | None = None
    wechatId: str | None = None
    status: str | None = None


class GuideFaqItem(LyraModel):
    question: str
    answer: str


class GuideListItem(LyraModel):
    slug: str
    title: str
    description: str
    coverImage: str | None = None
    readingMinutes: int | None = None
    updatedAt: str
    tags: list[str] = Field(default_factory=list)


class GuidesListResponse(LyraModel):
    items: list[GuideListItem]
    page: int
    pageSize: int
    total: int


class GuideDetail(GuideListItem):
    body: str
    seoTitle: str | None = None
    seoDescription: str | None = None
    wordCount: int | None = None
    legacySlugs: list[str] = Field(default_factory=list)
    faq: list[GuideFaqItem] = Field(default_factory=list)
    publishedAt: str | None = None


class ExperienceListItem(LyraModel):
    id: str
    publicId: str
    type: str
    status: str
    title: str
    summary: str | None = None
    province: str | None = None
    city: str | None = None
    themeTags: list[str] = Field(default_factory=list)


class ExperienceOccurrence(LyraModel):
    id: str
    status: str
    titleOverride: str | None = None
    dateText: str | None = None
    meetingPointText: str | None = None
    hostName: str | None = None


class ExperienceLinkedPoi(LyraModel):
    poiId: str
    poiName: str
    role: str
    notes: str | None = None


class ExperienceDetail(ExperienceListItem):
    titleZh: str | None = None
    titleEn: str | None = None
    description: str | None = None
    experienceMode: str
    bookingMode: str
    priceMode: str
    durationText: str | None = None
    highlights: list[str] = Field(default_factory=list)
    occurrences: list[ExperienceOccurrence] = Field(default_factory=list)
    linkedPois: list[ExperienceLinkedPoi] = Field(default_factory=list)


class ExperienceListResponse(LyraModel):
    items: list[ExperienceListItem]
    page: int
    pageSize: int
    total: int


class RestaurantDetail(LyraModel):
    id: str
    type: str | None = None
    destinationId: str | None = None
    name: str
    image: str | None = None
    photoUrl: str | None = None
    cuisineType: str | None = None
    recommendedDishes: list[str] = Field(default_factory=list)
    address: str | None = None
    lat: float | str | None = None
    lng: float | str | None = None
    nearbyTransport: str | None = None
    phone: str | None = None
    openingHours: str | None = None
    mustEatIndex: float | str | None = None
    avgCost: str | None = None
    queueStatus: str | None = None
    nearbyAttractions: list[str] = Field(default_factory=list)
    priceRange: str | None = None
    rating: float | str | None = None
    tags: list[str] = Field(default_factory=list)


class DestinationListItem(LyraModel):
    id: str
    slug: str
    name: str
    description: str
    longDescription: str | None = None
    province: str | None = None
    city: str | None = None
    tourCount: int
    image: str | None = None


class Attraction(LyraModel):
    id: str
    type: str | None = None
    name: str
    image: str | None = None
    tags: list[str] = Field(default_factory=list)
    reason: str | None = None
    rating: float | None = None
    topReview: str | None = None
    nameZh: str | None = None
    nameEn: str | None = None
    region: str | None = None
    address: str | None = None
    category: str | None = None
    nearbyTransport: str | None = None
    openingHours: str | None = None
    ticketPrice: str | None = None
    suggestedDuration: str | None = None
    bestVisitDate: str | None = None
    introduction: str | None = None
    suitableFor: list[str] = Field(default_factory=list)
    sellingPoints: list[str] = Field(default_factory=list)
    photos: list[str] = Field(default_factory=list)


class Food(LyraModel):
    id: str
    name: str
    image: str | None = None
    tags: list[str] = Field(default_factory=list)
    priceRange: str | None = None
    reviews: int | None = None
    reason: str | None = None
    topReview: str | None = None
    restaurantName: str | None = None
    restaurantAddress: str | None = None
    restaurantId: str | None = None
    phone: str | None = None
    nearbyTransport: str | None = None
    openingHours: str | None = None
    mustEatIndex: float | str | None = None
    avgCost: str | None = None
    queueStatus: str | None = None


class DestinationRestaurant(LyraModel):
    id: str
    type: str | None = None
    destinationId: str
    name: str
    image: str | None = None
    photoUrl: str | None = None
    cuisineType: str | None = None
    recommendedDishes: list[str] = Field(default_factory=list)
    address: str | None = None
    lat: float | str | None = None
    lng: float | str | None = None
    nearbyTransport: str | None = None
    phone: str | None = None
    openingHours: str | None = None
    mustEatIndex: float | str | None = None
    avgCost: str | None = None
    queueStatus: str | None = None
    nearbyAttractions: list[str] = Field(default_factory=list)
    priceRange: str | None = None
    rating: float | str | None = None
    tags: list[str] = Field(default_factory=list)


class Hotel(LyraModel):
    id: str
    type: str | None = None
    name: str
    address: str | None = None
    lat: float | str | None = None
    lng: float | str | None = None
    starLevel: int | None = None
    priceRange: str | None = None
    rating: float | str | None = None
    amenities: dict[str, Any] | None = None
    tags: list[str] = Field(default_factory=list)
    image: str | None = None


class DestinationDetail(DestinationListItem):
    attractions: list[Attraction] = Field(default_factory=list)
    famousFoods: list[Food] = Field(default_factory=list)
    restaurants: list[DestinationRestaurant] = Field(default_factory=list)
    hotels: list[Hotel] = Field(default_factory=list)


class DestinationListResponse(LyraModel):
    items: list[DestinationListItem]
    page: int
    pageSize: int
    total: int


class RouteSummary(LyraModel):
    id: str
    routeName: str
    routeAlias: str | None = None
    routeStyle: str | None = None
    price: float | str | None = None
    priceUnit: str | None = None
    highlights: list[str] = Field(default_factory=list)
    coverImages: list[str] = Field(default_factory=list)
    totalDays: int
    status: int | None = None


class RouteTransportNode(LyraModel):
    fromLocation: str | None = None
    toLocation: str | None = None
    transportMethod: str | None = None
    routeDetail: str | None = None
    cost: float | str | None = None
    notes: str | None = None


class RoutePoiNode(LyraModel):
    id: str
    type: str
    name: str
    address: str | None = None
    openingHours: str | None = None
    ticketPrice: str | None = None
    suggestedDuration: str | None = None
    description: str | None = None
    highlights: list[dict[str, Any]] = Field(default_factory=list)
    primaryImage: str | None = None
    gallery: list[str] = Field(default_factory=list)
    phone: str | None = None
    avgCost: float | str | None = None
    queueStatus: str | None = None
    notes: str | None = None


class RouteNode(LyraModel):
    id: str
    dayId: str
    nodeOrder: int
    nodeType: str
    startTime: str | None = None
    durationMinutes: int | None = None
    transport: RouteTransportNode | None = None
    poi: RoutePoiNode | None = None


class RouteDay(LyraModel):
    id: str
    dayNumber: int
    dayTitle: str | None = None
    daySubtitle: str | None = None
    nodes: list[RouteNode] = Field(default_factory=list)


class RouteDetail(RouteSummary):
    recommendation: str | None = None
    introduction: str | None = None
    routeOverview: str | None = None
    serviceContent: str | None = None
    days: list[RouteDay] = Field(default_factory=list)


class RoutesListResponse(LyraModel):
    items: list[RouteSummary]
    page: int
    pageSize: int
    total: int
