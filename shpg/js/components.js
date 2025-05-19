function generateUUID() {
    var d = new Date().getTime();
    //Time in microseconds since page-load or 0 if unsupported
    var d2 = ((typeof performance !== 'undefined') && performance.now && (performance.now()*1000)) || 0;
    return 'xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        //random number between 0 and 16
        var r = Math.random() * 16;
        if(d > 0){
            //Use timestamp until depleted
            r = (d + r)%16 | 0;
            d = Math.floor(d/16);
        } else {
            //Use microseconds since page-load if supported
            r = (d2 + r)%16 | 0;
            d2 = Math.floor(d2/16);
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}


/**
 * Abstract HTML renderable Class
 *
 * @class HTMLComponent
 */
class HTMLComponent {
    constructor(el) {
        this.element = el
        this.id = generateUUID()
    }
    
    html() {
        throw new Error("Method 'html()' must be implemented.");
    }

    render(){
        if(!this.element) {
            throw new Error(`Undefined HTML element.`)
        }
        this.element.innerHTML = this.html()
    }
}


/**
 *  ImgSlider show two images and a slider
 *  to manually view one or an other at the same
 *  place
 */
class ImgSlider extends HTMLComponent {
    ratio = 0
    ctx = null
    img1 = null
    img2 = null
    updateRatio = false
    
    constructor(el, img1, img2, title=null, width=0, height=0, onMountedCallback=null, onRatioChangedCallback=null) {
        super(el)
        this.img1Path = img1
        this.img2Path = img2
        this.width = width
        this.height = height
        this.onMountedCallback = onMountedCallback
        this.onRatioChangedCallback = onRatioChangedCallback
        this.render()
        this.init()
    }

    init() {
        this.img1 = new Image()
        this.img1.src = this.img1Path
        this.img1.onload = function() {
            let doRender = false
            if(this.width == 0) { this.width = this.img1.naturalWidth; doRender=true}
            if(this.height == 0) { this.height = this.img1.naturalHeight; doRender=true}
            if(doRender) this.render()

            const canvas = document.getElementById(this.id)
            this.ctx = canvas.getContext("2d")
            this.img2 = new Image()
            this.img2.src = this.img2Path
            this.img2.onload = function() {
                this.setRatio(0)
                addEventListener("mousedown", this.onMouseDown.bind(this));
                addEventListener("mouseup", this.onMouseUp.bind(this));
                addEventListener("mousemove", this.onMouseMove.bind(this));
                if(this.onMountedCallback) this.onMountedCallback()
            }.bind(this)
        }.bind(this)
    }

    setRatio(r) {
        if(r < 0) r = 0;
        else if(r > 1) r = 1;
        this.ratio = r
        this.draw()
    }
    onMouseDown(event) {
        this.updateRatio = true
        this.update(event.clientX, event.clientY)
    }
    onMouseUp(event) {
        this.updateRatio = false
        this.draw()
    }
    onMouseMove(event) {
        if(!this.updateRatio) return
        this.update(event.clientX, event.clientY)
    }
    update(x, y) {
        const area = this.element.getBoundingClientRect()
        if(x >= area.x && x < area.x+area.width && y >= area.y && y < area.y+area.height) {
            this.setRatio( (x - area.x) / this.width )
            if(this.onRatioChangedCallback) this.onRatioChangedCallback(this.id, this.ratio)
        }
    }

    draw() {
        if(!this.img1 || !this.img2) console.warn("Images are not load.")
        const ctx = this.ctx
        const clipX = this.width * this.ratio

        ctx.clearRect(0, 0, this.width, this.height)
        ctx.save()
        ctx.drawImage(this.img1, 0, 0, this.width, this.height); 
        ctx.rect(clipX, 0, this.width-clipX, this.height);
        ctx.clip();
        ctx.drawImage(this.img2, 0, 0, this.width, this.height);
        ctx.restore()
        ctx.beginPath()
        if(this.updateRatio) {
            ctx.rect(clipX, 0, 1, this.height)
            ctx.fillStyle="white"
            ctx.fill()
        }
    }

    html() {
        return `
            <div class="image-slider">
                <p class="image-slider-title">Title</p>
                <canvas 
                    class="image-slider-canvas" 
                    id="${this.id}" 
                    width="${this.width}px" 
                    height="${this.height}px">
                </canvas>
            </div>
        `
    }
}
