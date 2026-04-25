import asyncio

import pytest
import httpx

from lyra import (
    AsyncLyraClient,
    LyraAuthenticationError,
    LyraResponseValidationError,
    LyraServerError,
)


def test_route_page_summary_sends_bearer_token_and_parses_typed_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers.get("authorization")
        return httpx.Response(
            200,
            json={
                "route_id": "premium-china",
                "summary": {
                    "routePageId": "premium-china",
                    "slug": "premium-china",
                    "title": {"en": "Premium China", "zh": "品质中国"},
                    "subtitle": {"en": "12-day tour", "zh": "12天行程"},
                    "price": 5375,
                    "image": "https://cdn.lyriktrip.com/cover.webp",
                    "highlights": ["Shanghai"],
                    "duration": 12,
                    "group": 12,
                    "status": "active",
                },
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        api_key="test-token",
        transport=httpx.MockTransport(handler),
    )

    summary = asyncio.run(client.route_v2.summary("premium-china"))

    assert summary is not None
    assert summary.routePageId == "premium-china"
    assert summary.title.zh == "品质中国"
    assert seen == {
        "url": "http://datapipe.test/api/v1/query/route-page/premium-china",
        "authorization": "Bearer test-token",
    }


def test_route_page_list_parses_summary_collection() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "routePageId": "premium-china",
                        "slug": "premium-china",
                        "title": {"en": "Premium China", "zh": "品质中国"},
                        "subtitle": {"en": "12-day tour", "zh": "12天行程"},
                        "price": 5375,
                        "image": "https://cdn.lyriktrip.com/cover.webp",
                        "highlights": ["Shanghai"],
                        "duration": 12,
                        "group": 12,
                        "status": "active",
                    }
                ]
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.list())

    assert result.items[0].routePageId == "premium-china"
    assert result.items[0].title.zh == "品质中国"
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-pages"


def test_route_page_journey_parses_module_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "routePageId": "premium-china",
                "hero": {
                    "title": {"en": "Premium China", "zh": "品质中国"},
                    "subtitle": {"en": "12-day tour", "zh": "12天行程"},
                    "tags": [],
                    "metrics": {
                        "durationDays": 12,
                        "basePriceUsd": 5375,
                        "groupSize": 12,
                        "rating": 5,
                    },
                },
                "selling_points": [
                    {"en": "Shanghai", "zh": "上海"},
                ],
                "map_image": None,
                "city_highlights": [
                    {
                        "city_id": "shanghai",
                        "city_name": {"en": "Shanghai", "zh": "上海"},
                        "city_subtitle": {"en": "Neon nights", "zh": "霓虹夜色"},
                        "days": 2,
                        "image": None,
                        "map_coords": None,
                    }
                ],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.journey("premium-china"))

    assert result is not None
    assert result.routePageId == "premium-china"
    assert result.hero.metrics.durationDays == 12
    assert result.city_highlights[0].city_name.zh == "上海"
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-page/premium-china/journey"


def test_route_page_itinerary_parses_module_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "routePageId": "premium-china",
                "themes": [
                    {
                        "id": "composition_theme__urban-pulse",
                        "title": {"en": "Urban Pulse", "zh": "都市脉动"},
                        "subtitle": {
                            "en": "Skyscrapers and lane houses in one frame.",
                            "zh": "摩天楼与百年石库门在同一坐标共存。",
                        },
                        "days": 2,
                        "cities": [
                            {
                                "city_id": "shanghai",
                                "city_name": {"en": "Shanghai", "zh": "上海"},
                                "days": 2,
                                "city_subtitle": {
                                    "en": "Where East meets West in neon",
                                    "zh": "霓虹中的东西交汇",
                                },
                                "city_rec": {
                                    "en": "The gateway that rewires expectations.",
                                    "zh": "重塑第一印象的中国入口。",
                                },
                                "city_guide": {
                                    "en": "Your first two days set the tone.",
                                    "zh": "最初两天为整段旅程定下节奏。",
                                },
                                "transports": {"en": "Flight · 1.5 hours", "zh": "航班 · 1.5小时"},
                                "transmodel": "fly",
                                "imgs": [],
                            }
                        ],
                    }
                ],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.itinerary("premium-china"))

    assert result is not None
    assert result.routePageId == "premium-china"
    assert result.themes[0].title.zh == "都市脉动"
    assert result.themes[0].cities[0].transports is not None
    assert result.themes[0].cities[0].transports.zh == "航班 · 1.5小时"
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-page/premium-china/itinerary"


def test_route_page_hotels_parses_module_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "routePageId": "premium-china",
                "items": [
                    {
                        "name": {"en": "The PuLi Hotel", "zh": "The PuLi Hotel"},
                        "city": {"en": "Shanghai", "zh": "Shanghai"},
                        "location": None,
                        "nights": 2,
                        "description": {
                            "en": "Urban retreat with spa and dining.",
                            "zh": "Urban retreat with spa and dining.",
                        },
                        "image": "https://cdn.lyriktrip.com/hotels/puli.jpg",
                        "featured": False,
                    }
                ],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.hotels("premium-china"))

    assert result is not None
    assert result.routePageId == "premium-china"
    assert result.items[0].name.en == "The PuLi Hotel"
    assert result.items[0].nights == 2
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-page/premium-china/hotels"


def test_route_page_experiences_parses_module_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "routePageId": "premium-china",
                "subheadline": {
                    "en": "Seven curated encounters with the people who make China unforgettable.",
                    "zh": "七段精心策划的人文相遇。",
                },
                "items": [
                    {
                        "city": {"en": "Shanghai", "zh": "上海"},
                        "tag": {"en": "Exclusive Access", "zh": "独家通道"},
                        "image": "https://cdn.lyriktrip.com/moments/shanghai-rooftop.jpg",
                        "title": {
                            "en": "The Bund & French Concession After Dark",
                            "zh": "夜幕下的外滩与法租界",
                        },
                        "subtitle": {
                            "en": "A privately opened rooftop perch.",
                            "zh": "仅限私人开放的顶层平台。",
                        },
                        "description": {
                            "en": "Your host grew up in the lanes behind the waterfront.",
                            "zh": "你的主理人就出生在这附近的弄堂里。",
                        },
                        "exclusiveAccess": {
                            "en": "Not open to the public.",
                            "zh": "此顶层不对外公开。",
                        },
                        "host": {
                            "name": {"en": "James", "zh": "詹姆斯"},
                            "role": {
                                "en": "Shanghai local · architectural historian",
                                "zh": "上海本地人，建筑史学家",
                            },
                            "bio": {
                                "en": "He knows every shikumen lane.",
                                "zh": "他熟知每条石库门弄堂。",
                            },
                            "avatarLabel": None,
                        },
                    }
                ],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.experiences("premium-china"))

    assert result is not None
    assert result.routePageId == "premium-china"
    assert result.subheadline is not None
    assert result.subheadline.zh == "七段精心策划的人文相遇。"
    assert result.items[0].host is not None
    assert result.items[0].host.name.zh == "詹姆斯"
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-page/premium-china/experiences"


def test_route_page_concierge_parses_module_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "routePageId": "premium-china",
                "id": "concierge_vivian_chen",
                "name": "Vivian Chen",
                "avatarInitials": "VC",
                "title": "Private Travel Concierge · Premium China",
                "tagline": "I'm not your tour guide. I'm the person who makes sure nothing goes wrong — and everything goes right.",
                "bio": "Born in Shanghai, raised between Beijing and San Francisco.",
                "stats": [
                    {"n": "12", "label": "Years"},
                    {"n": "500+", "label": "Journeys"},
                    {"n": "4h", "label": "Response"},
                ],
                "languages": ["English", "中文", "Cantonese"],
                "isOnline": True,
                "onlineLabel": "Online",
                "wechatId": "PremiumChinaVivian",
                "status": "active",
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.route_v2.concierge("premium-china"))

    assert result is not None
    assert result.routePageId == "premium-china"
    assert result.avatarInitials == "VC"
    assert result.languages[2] == "Cantonese"
    assert result.wechatId == "PremiumChinaVivian"
    assert seen["url"] == "http://datapipe.test/api/v1/query/route-page/premium-china/concierge"


def test_experiences_list_parses_typed_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "experience__water-splashing-festival",
                        "publicId": "exp_festival_1",
                        "type": "festival",
                        "status": "active",
                        "title": "傣族泼水节",
                        "summary": "西双版纳代表性民族节庆体验。",
                        "province": "Yunnan",
                        "city": "Xishuangbanna",
                        "themeTags": ["festival", "ethnic"],
                    }
                ],
                "page": 1,
                "pageSize": 12,
                "total": 1,
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.experiences.list(page=1, page_size=12, q="festival"))

    assert result.items[0].publicId == "exp_festival_1"
    assert result.items[0].themeTags == ["festival", "ethnic"]
    assert seen["url"] == "http://datapipe.test/api/v1/query/experiences?page=1&pageSize=12&q=festival"


def test_experience_detail_parses_typed_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "id": "experience__water-splashing-festival",
                "publicId": "exp_festival_1",
                "type": "festival",
                "status": "active",
                "title": "傣族泼水节",
                "titleZh": "傣族泼水节",
                "titleEn": "Water Splashing Festival",
                "summary": "西双版纳代表性民族节庆体验。",
                "description": "每年重要节庆活动。",
                "experienceMode": "seasonal",
                "bookingMode": "content_only",
                "priceMode": "free",
                "durationText": "3天",
                "province": "Yunnan",
                "city": "Xishuangbanna",
                "themeTags": ["festival", "ethnic"],
                "highlights": ["泼水巡游"],
                "occurrences": [
                    {
                        "id": "occ_1",
                        "status": "scheduled",
                        "titleOverride": "2026 西双版纳泼水节",
                        "dateText": "2026-04-13 至 2026-04-15",
                        "meetingPointText": "泼水广场北门",
                        "hostName": "西双版纳文旅局",
                    }
                ],
                "linkedPois": [
                    {
                        "poiId": "poi_xishuangbanna_square",
                        "poiName": "泼水广场",
                        "role": "venue",
                        "notes": "主会场",
                    }
                ],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.experiences.get("exp_festival_1"))

    assert result is not None
    assert result.publicId == "exp_festival_1"
    assert result.occurrences[0].titleOverride == "2026 西双版纳泼水节"
    assert seen["url"] == "http://datapipe.test/api/v1/query/experience/exp_festival_1"


def test_restaurant_detail_parses_typed_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "id": "poi_duck_house",
                "type": "restaurant",
                "destinationId": "dest_beijing",
                "name": "Duck House",
                "image": "https://cdn.lyriktrip.com/restaurants/duck-house.webp",
                "photoUrl": "https://cdn.lyriktrip.com/restaurants/duck-house.webp",
                "cuisineType": "Beijing cuisine",
                "recommendedDishes": ["Peking Duck"],
                "address": "Somewhere in Beijing",
                "lat": "39.9042",
                "lng": "116.4074",
                "nearbyTransport": "Metro Line 8",
                "phone": "12345678",
                "openingHours": "10:00-22:00",
                "mustEatIndex": "4.5",
                "avgCost": "200 CNY",
                "queueStatus": "busy",
                "nearbyAttractions": ["Temple of Heaven"],
                "priceRange": "$$",
                "rating": "4.7",
                "tags": ["roast duck"],
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.restaurants.get("poi_duck_house"))

    assert result is not None
    assert result.id == "poi_duck_house"
    assert result.cuisineType == "Beijing cuisine"
    assert seen["url"] == "http://datapipe.test/api/v1/query/restaurant/poi_duck_house"


def test_guides_list_sends_query_params_and_parses_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "slug": "beijing-food-guide",
                        "title": "Beijing Food Guide",
                        "description": "Where to eat in Beijing",
                        "coverImage": "https://cdn.lyriktrip.com/guides/beijing-food-guide.webp",
                        "readingMinutes": 8,
                        "updatedAt": "2026-04-21T00:00:00Z",
                        "tags": ["food"],
                    }
                ],
                "page": 1,
                "pageSize": 10,
                "total": 1,
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.guides.list(page=1, page_size=10, q="", tag=""))

    assert result.items[0].slug == "beijing-food-guide"
    assert result.items[0].readingMinutes == 8
    assert seen["url"] == "http://datapipe.test/api/v1/query/guides?page=1&pageSize=10&q=&tag="


def test_guide_detail_parses_payload() -> None:
    seen: dict[str, object] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "slug": "beijing-food-guide",
                "title": "Beijing Food Guide",
                "description": "Where to eat in Beijing",
                "coverImage": "https://cdn.lyriktrip.com/guides/beijing-food-guide.webp",
                "readingMinutes": 8,
                "updatedAt": "2026-04-21T00:00:00Z",
                "tags": ["food"],
                "body": "## Body",
                "seoTitle": "Beijing Food Guide",
                "seoDescription": "Where to eat in Beijing",
                "wordCount": 1200,
                "legacySlugs": ["beijing-legacy-guide"],
                "faq": [{"question": "Q", "answer": "A"}],
                "publishedAt": "2026-04-20T00:00:00Z",
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(client.guides.get("beijing-food-guide"))

    assert result is not None
    assert result.slug == "beijing-food-guide"
    assert result.seoTitle == "Beijing Food Guide"
    assert seen["url"] == "http://datapipe.test/api/v1/query/guide/beijing-food-guide"


def test_destination_list_sends_query_params() -> None:
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "dest_beijing",
                        "slug": "dest_beijing",
                        "name": "Beijing",
                        "description": "Capital city",
                        "longDescription": None,
                        "province": "Beijing",
                        "city": "Beijing",
                        "tourCount": 12,
                        "image": None,
                    }
                ],
                "page": 2,
                "pageSize": 10,
                "total": 1,
            },
        )

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    result = asyncio.run(
        client.destinations.list(
            page=2,
            page_size=10,
            q="bei",
            province="Beijing",
        )
    )

    assert result.items[0].id == "dest_beijing"
    assert seen["url"] == (
        "http://datapipe.test/api/v1/query/destinations?"
        "page=2&pageSize=10&q=bei&province=Beijing"
    )


def test_retrieve_returns_none_for_404() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "missing"})

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    assert asyncio.run(client.routes.get("missing-route")) is None


def test_authentication_errors_are_mapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"detail": "bad token"})

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(LyraAuthenticationError) as exc_info:
        asyncio.run(client.routes.list())

    assert exc_info.value.status_code == 403
    assert str(exc_info.value) == "bad token"


def test_server_errors_are_mapped() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="upstream unavailable")

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(LyraServerError) as exc_info:
        asyncio.run(client.destinations.list())

    assert exc_info.value.status_code == 503


def test_invalid_response_shape_raises_validation_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"items": "not-a-list"})

    client = AsyncLyraClient(
        base_url="http://datapipe.test",
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(LyraResponseValidationError):
        asyncio.run(client.routes.list())
