<script>
    import {onMount} from "svelte";

    let canvas;
    let context;
    let level;
    let recorddate = "-:-:- -.-.-";
    let canvasSize = 200;
    let tankRadius = 95;
    let waterlevelPercentage = 0;

    function fillCircle(x, y, radius, color) {
        context.fillStyle = color;
        context.beginPath();
        context.arc(x, y, radius, 0, 2 * Math.PI);
        context.fill();
    }

    function drawBorder(x, y, radius, color) {
        context.beginPath();
        context.fillStyle = color;
        context.lineWidth = 5;
        context.arc(x, y, radius, 0, 2 * Math.PI);
        context.stroke();
    }

    function drawRectangle(width, height, color) {
        context.beginPath();
        context.fillStyle = color;
        context.lineWidth = 5;
        context.rect(0, 0, width, height)
        context.fill();
    }

    function drawPercentage(x1,x2,x3, y) {
        context.beginPath();
        context.fillStyle = 'black';
        context.font = "48px sans-serif";
        let x = x1;
        if(waterlevelPercentage<100)
            x=x2;
        if(waterlevelPercentage<10)
            x=x3;
        context.fillText(waterlevelPercentage + "%", x, y);
    }

    async function getLevelData() {
        let url = window.location.origin
        try {
            const res = await fetch(url + "/api/water-level/get");
            const response_data = await res.json();
            console.log(response_data);
            level = response_data["Level"];
            let dateFormat = new Date(parseInt(response_data["RowKey"]) * 1000);
            console.log(level);

            recorddate = dateFormat.getDate() +
                "." + (dateFormat.getMonth() + 1) +
                "." + dateFormat.getFullYear() +
                " " + dateFormat.getHours() +
                ":" + dateFormat.getMinutes() +
                ":" + dateFormat.getSeconds();
            console.log(recorddate);
        } catch (error) {
            console.log(error);
        }

    }

    function calculatePercentageWaterLevel() {
        let r = 100;
        let tempWaterLevel = (r * 2 / 100) * (level);
        console.log("tempWaterLevel: "+tempWaterLevel);
        let area = Math.round(3.14 * r * r);
        let unitArea = area / 360;
        let onePercentageArea = area / 100;
        console.log("area: " + area);
        console.log("unitArea: " + unitArea);

        if (level >= 100) {
            console.log("plno");
            return level;
        } else if (level > 50) {
            let h = tempWaterLevel-r;
            // console.log("h: " + h);
            let angel = Math.round((Math.acos(h / r)) / (Math.PI / 180) * 2);
            // console.log("angel: " + angel);
            let circularSection = unitArea * angel;
            // console.log("circularSection: " + circularSection);
            let t = (r * Math.sin(Math.round(angel / 2) * (Math.PI / 180))) * 2;
            // console.log("t: " + t);
            let triangleArea = h * t / 2;
            // console.log("triangleArea: " + triangleArea);
            console.log("hodne");
            return 100-((circularSection - triangleArea) / onePercentageArea);

        } else if (level < 50) {
            let h = r - tempWaterLevel;
            // console.log("h: " + h);
            let angel = Math.round((Math.acos(h / r)) / (Math.PI / 180) * 2);
            // console.log("angel: " + angel);
            let circularSection = unitArea * angel;
            // console.log("circularSection: " + circularSection);
            let t = (r * Math.sin(Math.round(angel / 2) * (Math.PI / 180))) * 2;
            // console.log("t: " + t);
            let triangleArea = h * t / 2;
            // console.log("triangleArea: " + triangleArea);
            console.log("malo");
            return (circularSection - triangleArea) / onePercentageArea;
        } else {
            console.log("pulka");
            return 50;
        }
    }

    onMount(async () => {
        await getLevelData();
        canvas = document.querySelector('#tank-canvas');
        context = canvas.getContext('2d');
        fillCircle(100, 100, tankRadius, 'dodgerblue');

        waterlevelPercentage = Math.round(calculatePercentageWaterLevel());
        console.log("level: " + (canvasSize / 100) * (level) + " " + (canvasSize / 100) + " " + (100 - level) + " " + waterlevelPercentage)
        drawRectangle(200, (canvasSize / 100) * (100 - level), "white");
        drawBorder(100, 100, tankRadius, 'black');
        drawPercentage(40,60,70, 118);
    });

</script>

<main>
    <h1>Water Controller</h1>
    <canvas id="tank-canvas" width={canvasSize} height={canvasSize}></canvas>
    <h2>Datum měření: {recorddate}</h2>
</main>

<style>
    main {
        text-align: center;
        align-content: center;
        max-width: 240px;
        margin: 0 auto;
    }


    h1 {
        color: dodgerblue;
        text-align: center;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 450px) {
        main {
            max-width: none;
        }
    }

    @media (max-width: 450px) {
        h1 {
            font-size: 10mm;
        }
    }

</style>