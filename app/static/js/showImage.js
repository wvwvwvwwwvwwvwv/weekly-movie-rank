function showImage(str) {
        const value = parseInt(str);
        const image = document.getElementById('image');
        var imageUrl = `../static/pictures/${movieId}{type}worldcloud.png`;
        if (value === 5 || value === 4) {
          imageUrl = imageUrl.replace("{type}", "h");
          image.alt = 'star5-4';
        } else if (value === 3) {
          imageUrl = imageUrl.replace("{type}", "m");
          image.alt = 'star3';
        } else {
          imageUrl = imageUrl.replace("{type}", "l");
          image.alt = 'star2-1';
        }
        image.src = imageUrl;
      }